import click
from . import dude_cli
from .cli_base import _init_env_toolbox, _pass_env_toolbox


@dude_cli.group("app")
@click.pass_context
def app_group(ctx):
    ctx.obj = _init_env_toolbox(ctx)


@app_group.command("run")
@_pass_env_toolbox
@click.option("--skip-sync", is_flag=True)
@click.argument("run-args", nargs=-1, type=str)
def run(env_toolbox, skip_topic_creation, skip_sync, run_args):
    env_toolbox.run_app(skip_topic_creation, skip_sync, run_args)


@app_group.command("sync")
@_pass_env_toolbox
@click.option("--wipe-existing", is_flag=True)
def sync(env_toolbox, wipe_existing):
    env_toolbox.sync_venv(wipe_existing)


@click.option("--skip-sync", is_flag=True)
@click.argument("extra_pytest_args", nargs=-1, type=click.UNPROCESSED)
@app_group.command("unit_test", context_settings={"ignore_unknown_options": True})
@_pass_env_toolbox
def unit_test(env_toolbox, extra_pytest_args, skip_sync):
    env_toolbox.run_unit_tests(extra_pytest_args=list(extra_pytest_args), skip_sync=skip_sync)


@click.option("--skip-sync", is_flag=True)
@click.argument("extra_pytest_args", nargs=-1, type=click.UNPROCESSED)
@app_group.command("integration_test", context_settings={"ignore_unknown_options": True})
@_pass_env_toolbox
def integration_test(env_toolbox, extra_pytest_args, skip_sync):
    env_toolbox.run_integration_tests(extra_pytest_args=list(extra_pytest_args), skip_sync=skip_sync)


@app_group.command("build_reqs")
@_pass_env_toolbox
def build_requirements(env_toolbox):
    env_toolbox.build_reqs()
