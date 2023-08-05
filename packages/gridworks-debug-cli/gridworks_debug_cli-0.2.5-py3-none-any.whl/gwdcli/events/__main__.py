import asyncio
import atexit
import logging
import shutil
from pathlib import Path
from typing import List
from typing import Optional

import rich
import typer
from anyio import create_task_group
from anyio import run
from rich.console import Console

from gwdcli.events.mqtt import run_mqtt_client
from gwdcli.events.queue_loop import AsyncQueueLooper
from gwdcli.events.settings import EventsSettings
from gwdcli.events.settings import Paths
from gwdcli.events.show_dir import show_dir
from gwdcli.events.sync import sync
from gwdcli.events.tui import TUI


app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    rich_markup_mode="rich",
    help="Commands for monitoring GridWorks communication events.",
)
app.command("dir")(show_dir)

# For sphinx:
typer_click_object = typer.main.get_command(app)


@app.command()
def show(
    config_path: Path = Paths().config_path,
    verbose: int = typer.Option(0, "--verbose", "-v", count=True),
    snap: Optional[List[str]] = typer.Option(None, "--snap"),
    clean: bool = typer.Option(  # noqa
        False, "-c", "--clean", help="Delete the entire data directory."
    ),
    no_sync: bool = typer.Option(
        False,
        "--no-sync",
        help="Skip downloading data from S3. Only mqtt data will be monitored.",
    ),
    no_mqtt: bool = typer.Option(
        False,
        "--no-mqtt",
        help="Download data from S3 but do no live monitoring of mqtt.",
    ),
):
    """Live display of incoming scada events and status"""
    settings = EventsSettings.load(config_path)
    settings.verbosity += verbose
    settings.snaps += snap
    if clean:
        rich.print(f"Deleting {settings.paths.data_dir}")
        shutil.rmtree(settings.paths.data_dir)
    run(show_main, settings, Console(), not no_sync, not no_mqtt)


@app.command()
def info(config_path: Path = Paths().config_path):  # noqa: B008
    """Print current configuration."""

    rich.print("")
    rich.print(f"Config path: {config_path}")
    rich.print(f"Config path exists: {config_path.exists()}")
    rich.print("Current settings:")
    settings = EventsSettings.load(config_path)
    rich.print(settings)


@app.command()
def mkconfig(
    config_path: Path = Paths().config_path, force: bool = False  # noqa: B008
):
    """Create default config file for '[bold green]gwd events[/bold green]' command."""
    rich.print()
    if config_path.exists() and not force:
        rich.print(
            f":warning-emoji:    [orange_red1]Config path [/]{config_path} [orange_red1]already exists."
        )
        rich.print(":warning-emoji:    [orange_red1][bold]Doing nothing.")
        rich.print()
        rich.print("Use [bold] --force [/bold] to overwrite existing config file.")
    else:
        if config_path.exists():
            rich.print(
                f":warning-emoji:    [orange_red1][bold]Overwritting config file [/][/]{config_path}."
            )
        else:
            rich.print(f"Creating default config at {config_path}")
        Paths(config_path=config_path).mkdirs()
        with config_path.open("w") as f:
            f.write(EventsSettings().json(sort_keys=True, indent=2) + "\n")
        rich.print("Created:")
        settings = EventsSettings.load(config_path)
        rich.print(settings)
    rich.print()


@app.command()
def clean(
    config_path: Path = Paths().config_path,
):
    """Delete the _entire_ events data directory"""
    settings = EventsSettings.load(config_path)
    rich.print(f"Deleting {settings.paths.data_dir}")
    shutil.rmtree(settings.paths.data_dir)


# noinspection PyUnusedLocal
async def show_main(
    settings: EventsSettings,
    console: Console,
    do_sync: bool = True,
    do_mqtt: bool = True,
):
    settings.paths.mkdirs()
    logger = logging.getLogger("gwd.events")
    # if settings.paths.log_path.exists():
    #     settings.paths.log_path.unlink()
    file_handler = logging.FileHandler(settings.paths.log_path)
    file_handler.setFormatter(logging.Formatter("%(asctime)s  %(message)s"))
    logger.addHandler(file_handler)
    if settings.verbosity == 1:
        logger.setLevel(logging.INFO)
    elif settings.verbosity > 1:
        logger.setLevel(logging.DEBUG)
    logger.info(
        "\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    )
    logger.info("Starting gwd events show")
    logger.info(settings.json(sort_keys=True, indent=2))
    async_queue = asyncio.Queue()
    async with create_task_group() as tg:
        tui = TUI(settings)
        if do_mqtt:
            tg.start_soon(run_mqtt_client, settings.mqtt, async_queue)
        if do_sync:
            tg.start_soon(sync, settings, async_queue)
        tg.start_soon(AsyncQueueLooper.loop_task, settings, async_queue, tui.queue)
        tg.start_soon(tui.tui_task)


if __name__ == "__main__":
    atexit.register(lambda: print("\x1b[?25h"))
    app()
