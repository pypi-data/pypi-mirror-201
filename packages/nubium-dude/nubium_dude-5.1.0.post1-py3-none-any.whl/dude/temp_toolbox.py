import logging
import pty
import select
import subprocess
from multiprocessing import Process
from pathlib import Path
from shutil import rmtree, copy2
from time import sleep
from typing import List, Optional
from unittest.mock import patch

from dotenv import load_dotenv
from virtualenv import cli_run
from virtualenvapi.manage import VirtualEnvironment
import yaml
import os


LOGGER = logging.getLogger(__name__)


class EnvironmentTag(yaml.YAMLObject):
    yaml_tag = u'!Environment'

    @classmethod
    def from_yaml(cls, loader, node):
        return os.environ[node.value]


yaml.SafeLoader.add_constructor(EnvironmentTag.yaml_tag, EnvironmentTag.from_yaml)


def load_yaml_fp(fp):
    if fp.endswith('.yaml') or fp.endswith('.yml'):
        with open(fp, 'r') as f:
            data = yaml.safe_load(f)
            if 'data' in data:
                data = yaml.safe_load(data['data']['nubium-topics.yaml'])
    else:
        data = yaml.safe_load(fp)
    return data


class EnvToolBox:

    def run_app(self, skip_sync=None, run_args="", runtime_env_overrides=None):
        if not _is_nubium_app():
            return

        if not skip_sync:
            _sync_virtual_environment()
        # TODO load DUDE_APP_VENV from dude's ConfigManager
        venv_path = Path(os.environ.get("DUDE_APP_VENV", "./venv"))
        load_dotenv(Path(f'{os.path.abspath(venv_path)}/.env'), override=True)
        if not [f for f in run_args if '.py' in f]:
            run_args = ['app.py'] + list(run_args)
        process = Process(target=run_command_in_virtual_environment, args=("python3.8", run_args))
        if not runtime_env_overrides:
            runtime_env_overrides = {}
        with patch.dict('os.environ', runtime_env_overrides):
            process.start()
        return process.pid

    @staticmethod
    def sync_venv(wipe_existing):
        if _is_nubium_app():
            _sync_virtual_environment(wipe_existing=wipe_existing)

    @staticmethod
    def build_reqs():
        if _is_nubium_app() and _has_requirements_in():
            _ensure_virtual_environment_exists()
            run_command_in_virtual_environment("pip-compile")

    @staticmethod
    def run_unit_tests(extra_pytest_args: Optional[List[str]] = None, skip_sync=None):
        if extra_pytest_args is None:
            extra_pytest_args = []
        if _is_nubium_app():
            if not skip_sync:
                _sync_virtual_environment()
            run_command_in_virtual_environment("pytest", ["./tests/unit/", "-rA", "-v"] + extra_pytest_args)

    @staticmethod
    def run_integration_tests(extra_pytest_args: Optional[List[str]] = None, skip_sync=None):
        if extra_pytest_args is None:
            extra_pytest_args = []
        if _is_nubium_app():
            if not skip_sync:
                _sync_virtual_environment()
            venv_path = Path(os.environ.get("DUDE_APP_VENV", "./venv"))
            load_dotenv(Path(f'{os.path.abspath(venv_path)}/.env'), override=True)
            run_command_in_virtual_environment("pytest", ["./tests/integration/", "-rA", "-svv", "--log-cli-level=INFO"] + extra_pytest_args)


def _wait_on_futures_map(futures):
    for future in futures.values():
        future.result()
        assert future.done()
        sleep(.1)


def _is_nubium_app():
    return Path("app.py").is_file()


def _has_requirements_in():
    return Path("requirements.in").is_file()


def _sync_virtual_environment(wipe_existing=False):
    venv_path = _ensure_virtual_environment_exists(wipe_existing)
    run_command_in_virtual_environment("pip-sync")
    # TODO merge these .env files to support bringing in new variables without overwriting existing customizations (see dotenv's CLI list command)
    local_dotenv = Path("configs/local.env")
    venv_dotenv = Path(f"{venv_path}/.env")
    if local_dotenv.is_file() and not venv_dotenv.is_file():
        copy2(local_dotenv, venv_dotenv)


def _ensure_virtual_environment_exists(wipe_existing: bool = False) -> Path:
    venv_path = Path(os.environ.get("DUDE_APP_VENV", "./venv"))
    if wipe_existing:
        rmtree(venv_path)
    venv_path.mkdir(parents=True, exist_ok=True)
    # TODO load python version from configuration
    cli_run([str(venv_path), "-p", "python3.8"])
    venv = VirtualEnvironment(str(venv_path), readonly=True)
    if not venv.is_installed("pip-tools"):
        # TODO lock versions of pip-tools and dependencies
        run_command_in_virtual_environment("pip", args=["install", "pip-tools"])
    return venv_path


def run_command_in_virtual_environment(command: str = "", args: List[str] = None):
    if not args:
        args = []
    venv_path = Path(os.environ.get("DUDE_APP_VENV", "./venv"))
    run_command_in_pseudo_tty(command=str(venv_path / "bin" / command), args=args)


def run_command_in_pseudo_tty(
        command: str,
        args: List[str] = None,
        output_handler=lambda data: print(data.decode("utf-8"), end=""),
        buffer_limit=512,
        buffer_timeout_seconds=0.04,
):
    # In order to get colored output from a command, the process is unfortunately quite involved.
    # Constructing a pseudo terminal interface is necessary to fake most commands into thinking they are in an environment that supports colored output
    if not args:
        args = []

    # It's possible to handle stderr separately by adding p.stderr.fileno() to the rlist in select(), and setting stderr=subproccess.PIPE
    # which would enable directing stderr to click.echo(err=True)
    # probably not worth the additional headache
    master_fd, slave_fd = pty.openpty()
    proc = subprocess.Popen([command] + args, stdin=slave_fd, stdout=slave_fd, stderr=subprocess.STDOUT, close_fds=True)

    def is_proc_still_alive():
        return proc.poll() is not None

    while True:
        ready, _, _ = select.select([master_fd], [], [], buffer_timeout_seconds)
        if ready:
            data = os.read(master_fd, buffer_limit)
            output_handler(data)
        elif is_proc_still_alive():  # select timeout
            assert not select.select([master_fd], [], [], 0)[0]  # detect race condition
            break  # proc exited
    os.close(slave_fd)  # can't do it sooner: it leads to errno.EIO error
    os.close(master_fd)
    proc.wait()
