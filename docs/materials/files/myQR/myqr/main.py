#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import sys

from rich.console import Console
import typer

DATE = "20 April 2026"
VERSION = "0.1.0"
AUTHOR = "myName"
AUTHORMAIL = "obonhamcarter@allegheny.edu"

cli = typer.Typer()
console = Console()


@cli.command()
def main(
    big_help_flag: bool = typer.Option(False, "--bighelp", help="Show extended help")
) -> None:
    """Front end of the program."""

    if big_help_flag:
        big_help()
        raise typer.Exit()

    console.print(
        "\t:dog:[bold yellow] QR code generator.\n\tStarting browser version. Use Control-C to exit from Command Line.[bold yellow]"
    )
    console.print(
        "\t:coffee:[bold green] Command: [bold yellow] Getting browser ready ..."
    )
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "myqr/myqr_streamlit.py"],
        check=False,
    )
# End of main()

def big_help() -> None:
    """Give available command line prompts."""

    h_str = "   " + DATE + " | version: " + VERSION + " |" + AUTHOR + " | " + AUTHORMAIL
    console.print(f"[bold green] {len(h_str) * '-'}")
    console.print(f"[bold yellow]{h_str}")
    console.print(f"[bold green] {len(h_str) * '-'}")
    console.print("\n\t:coffee:[bold green] Command: [bold yellow]uv run myqr")

# End of big_help()

def cli_entrypoint() -> None:
    """Package entrypoint for the myqr console script."""
    cli()
# End of cli_entrypoint()