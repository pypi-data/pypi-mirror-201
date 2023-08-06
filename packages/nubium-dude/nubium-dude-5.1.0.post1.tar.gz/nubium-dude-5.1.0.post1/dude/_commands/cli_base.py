import os
import runpy
import subprocess
import sys
import traceback

import click
from dude.temp_toolbox import EnvToolBox, run_command_in_pseudo_tty, run_command_in_virtual_environment
from dude._utils import ConfigManager, import_dotenvs


def _select_environment(ctx, param, value):
    if ctx.obj is None:
        ctx.obj = {}
    if value:
        ctx.obj["selected_environment"] = value
    return value


def _init_env_toolbox(ctx: click.Context) -> EnvToolBox:
    config_manager = ConfigManager()
    env = None
    try:
        env = ctx.obj.get("selected_environment", config_manager["default_environment"])
    except AttributeError:
        pass  # handled by the following condition
    if not env:
        raise click.BadParameter("No environment was selected")
    config_manager.activate_environment(env)
    return EnvToolBox()


_pass_env_toolbox = click.make_pass_decorator(EnvToolBox)


class LogUnexpectedExceptions(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except click.exceptions.Exit:
            raise
        except Exception:
            click.echo(traceback.format_exc(), err=True)
            click.get_current_context().exit(3)

    def invoke(self, *args, **kwargs):
        try:
            return super().invoke(*args, **kwargs)
        except click.exceptions.Exit:
            raise
        except Exception:
            click.echo(traceback.format_exc(), err=True)
            click.get_current_context().exit(3)


@click.group(invoke_without_command=True, cls=LogUnexpectedExceptions)
@click.option(
    "-e",
    "--environment",
    help="Overrides the default_enviroment defined by configuration",
    callback=_select_environment,
    expose_value=False,
)
@click.version_option(prog_name="dude", package_name="nubium-dude")
@click.pass_context
def dude_cli(ctx):
    if ctx.invoked_subcommand is None:
        print_help()
    else:
        import_dotenvs()


@dude_cli.command("format")
def auto_format():
    sys.argv[1:] = ["."]
    runpy.run_module("black")


@dude_cli.command("exec", context_settings=dict(allow_interspersed_args=False, ignore_unknown_options=True))
@click.pass_context
@click.argument("command", type=str)
@click.option("--use-venv", is_flag=True)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def run_command(ctx, use_venv, command, args):
    _init_env_toolbox(ctx)
    if use_venv:
        return run_command_in_virtual_environment(command=command, args=list(args))
    run_command_in_pseudo_tty(command, args=list(args))


@dude_cli.group(invoke_without_command=True, help="dump configuration", cls=LogUnexpectedExceptions)
@click.pass_context
def config(ctx):
    if ctx.invoked_subcommand is None:
        config_manager = ConfigManager()
        click.echo(config_manager)


@config.command("edit", help="Open dude's configuration in a text editor")
def config_edit():
    editor = os.environ.get("VISUAL", os.environ.get("EDITOR", "vi"))

    subprocess.call(
        [editor, ConfigManager.get_config_path().as_posix()],
    )


@dude_cli.command()
def lint():
    click.echo("TODO: run linter")


def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
