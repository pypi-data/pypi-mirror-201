#!/usr/bin/env python3

import logging
import os
import stat
import sys
from pathlib import Path

import click

RUN_CONFIGS_DIR: str = ".run_configs"


PathNotFoundError = Exception


def get_help_text(run_config: Path) -> str:
    # TODO: stub
    return str(run_config.absolute())


def get_base_dir() -> Path:
    cwd = Path(os.getcwd())
    try:
        rc_path = next(cwd.glob(RUN_CONFIGS_DIR))
        if rc_path.is_dir():
            return cwd
    except StopIteration:
        ...
    for path in cwd.parents:
        try:
            rc_path = next(path.glob(RUN_CONFIGS_DIR))
            if rc_path.is_dir():
                return path
        except StopIteration:
            ...
    raise click.UsageError(
        f"No {RUN_CONFIGS_DIR} found in current path or its parents."
    )


def get_rc_dir(base_dir: Path) -> Path:
    return base_dir / RUN_CONFIGS_DIR


def get_run_configs(base_dir: Path, incomplete: str = "") -> list[Path]:
    return [
        rc
        for rc in filter(
            lambda p: p.name.startswith(incomplete), get_rc_dir(base_dir).glob("**/*")
        )
        if rc.is_file() and os.access(str(rc.absolute()), os.X_OK)
    ]


class RunConfigType(click.ParamType):
    name = "run_config"

    def shell_complete(self, ctx, param, incomplete):
        try:
            base_dir = _get_param(ctx, "base_dir")
        except click.UsageError:
            _, exc_value, _ = sys.exc_info()
            logging.warning(exc_value)
            return []
        # return [click.shell_completion.CompletionItem(" ", help=exc_value)]
        return [
            click.shell_completion.CompletionItem(
                str(p.relative_to(get_rc_dir(base_dir))), help=get_help_text(p)
            )
            for p in get_run_configs(base_dir, incomplete)
        ]


def _get_param(ctx: click.Context, param: str) -> click.Parameter:
    if param in ctx.params:
        return ctx.params[param]
    if ctx.default_map is not None and param in ctx.default_map:
        return ctx.default_map[param]
    if (default_param := ctx.lookup_default(param)) is not None:
        return default_param
    for p in ctx.command.params:
        if p.name == param:
            return p.get_default(ctx)
    raise Exception(f"Could not find parameter {param}.")


def list_rc(ctx, _, value) -> None:
    if not value or ctx.resilient_parsing:
        return
    logging.debug("Listing run configs.")
    logging.debug(f"Parameter: {ctx.params}")
    base_dir = _get_param(ctx, "base_dir")
    commands = []
    help_texts = []
    for rc in get_run_configs(base_dir):
        commands.append(str(rc.relative_to(get_rc_dir(base_dir))))
        help_texts.append(get_help_text(rc))
    if not commands:
        logging.warning("No run configs found.")
        ctx.exit(0)
    longest_command = max(len(c) for c in commands)
    for command, help_text in zip(commands, help_texts):
        click.echo(f"{command.ljust(longest_command)}\t{help_text}")
    ctx.exit(0)


def print_zsh_completion(ctx, _, value) -> None:
    if not value or ctx.resilient_parsing:
        return
    logging.debug("Printing zsh completion.")
    logging.debug(f"Parameter: {ctx.params}")
    print('eval "$(_RC_COMPLETE=zsh_source rc)"')
    ctx.exit(0)


def print_base_dir(ctx, _, value) -> None:
    if not value or ctx.resilient_parsing:
        return
    logging.debug("Printing base dir.")
    logging.debug(f"Parameter: {ctx.params}")
    base_dir = _get_param(ctx, "base_dir")
    print(Path(base_dir).absolute())
    ctx.exit(0)


def print_rc_dir(ctx, _, value) -> None:
    if not value or ctx.resilient_parsing:
        return
    logging.debug("Printing run config dir.")
    logging.debug(f"Parameter: {ctx.params}")
    base_dir = _get_param(ctx, "base_dir")
    print(get_rc_dir(base_dir).absolute())
    ctx.exit(0)


def set_log_level(ctx, _, value) -> None:
    if not value or ctx.resilient_parsing:
        return
    logging.basicConfig(level=value, format="%(asctime)s │ %(levelname)-8s │ %(message)s")
    logging.debug(f"Setting log level to {value}.")
    return


@click.command()
@click.argument("run_config", type=RunConfigType())
@click.argument("args", nargs=-1)
@click.option(
    "--edit",
    "-e",
    is_flag=True,
    help="Edit run config instead of running.",
)
@click.option(
    "--list",
    "-l",
    "list_configs",
    is_flag=True,
    help="List available run configs.",
    callback=list_rc,
    expose_value=False,
    is_eager=True,
)
@click.option(
    "--make-executable",
    "-x",
    is_flag=True,
    help="Make run config executable if it isn't already.",
)
@click.option(
    "--base-dir",
    type=click.Path(exists=True, file_okay=False, readable=True, path_type=Path),
    default=get_base_dir,
    is_eager=True,
    help=(
        "Base directory to run from. Defaults to the first directory containing a .run_configs directory."
        " Should contain a .run_configs directory with executable run configs."
    ),
)
@click.option(
    "--get-base-dir",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    help="Print base directory.",
    callback=print_base_dir,
)
@click.option(
    "--get-rc-dir",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    help="Print run configuration directory.",
    callback=print_rc_dir,
)
@click.option(
    "--zsh-completion",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    help="Print zsh completion script.",
    callback=print_zsh_completion,
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    help="Log level.",
    is_eager=True,
    expose_value=False,
    callback=set_log_level,
)
@click.version_option()
@click.pass_context
def cli(
    ctx: click.Context,
    run_config: str,
    args: tuple[str],
    base_dir: Path,
    make_executable: bool = False,
    edit: bool = False,
) -> None:
    """Run a run config

    A run config can be any executable file in the .run_configs directory.
    """
    logging.debug(f"Parameter: {ctx.params}")
    rc_dir = get_rc_dir(base_dir)
    logging.debug(f"Base dir: {base_dir}")
    rc = rc_dir / run_config
    logging.debug(f"Run config: {rc}")
    if edit:
        editor = os.getenv("EDITOR", "vim")
        logging.debug(f"Editor: {editor}")
        logging.info(f"Editing {rc} with {editor}")
        if not rc.exists() and click.confirm(
            "Run config does not exist. Create?", default=True
        ):
            logging.debug(f"Creating {rc}")
            rc.touch()
            logging.debug(f"Making {rc} executable")
            os.chmod(
                str(rc.absolute()), os.stat(str(rc.absolute())).st_mode | stat.S_IEXEC
            )
        if not os.access(str(rc.absolute()), os.X_OK) and click.confirm(
            "Make executable?", default=True
        ):
            logging.debug(f"Making {rc} executable")
            os.chmod(
                str(rc.absolute()), os.stat(str(rc.absolute())).st_mode | stat.S_IEXEC
            )
        logging.debug(f"Opening {rc} with {editor}")
        os.execvp(editor, [editor, str(rc.absolute())])
    if not rc.exists():
        logging.error(f"Run config {run_config} does not exist in {rc_dir}.")
        raise click.UsageError(f"Run config {run_config} does not exist in {rc_dir}.")
    if not os.access(str(rc.absolute()), os.X_OK):
        if make_executable or click.confirm(
            "Run config not executable. Change permissions?", abort=True
        ):
            logging.debug(f"Making {rc} executable")
            os.chmod(
                str(rc.absolute()), os.stat(str(rc.absolute())).st_mode | stat.S_IEXEC
            )
    logging.debug(f"Changing directory to {base_dir}")
    os.chdir(base_dir)
    args_list = list(args) if len(args) > 0 else []
    logging.debug(f"Executing {rc} with args {args_list}")
    try:
        os.execv(str(rc.absolute()), [str(rc)] + args_list)
    except OSError as e:
        logging.error(f"Error executing {rc}: {e}")
        raise click.FileError(rc, f"{e}")


if __name__ == "__main__":
    cli()
