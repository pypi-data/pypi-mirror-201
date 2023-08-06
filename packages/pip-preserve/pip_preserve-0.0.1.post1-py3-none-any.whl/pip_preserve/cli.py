#!/usr/bin/env python3

import logging
import os
import site
import sys

import click
import daiquiri

_LOGGER = logging.getLogger(__name__)
daiquiri.setup(level=logging.INFO)


@click.command()
@click.option(
    "--site-packages",
    default=os.pathsep.join(site.getsitepackages()),
    show_default=True,
    metavar="DIRS",
    help=f"One or multiple site-packages directories to lookup provenance (separated with {os.pathsep!r}).",
)
@click.option(
    "--ignore-errors",
    is_flag=True,
    show_default=True,
    help="Ignore any errors while generating the requirements file.",
)
@click.option(
    "--debug",
    is_flag=True,
    show_default=True,
    help="Enable debug mode.",
)
@click.option(
    "--direct-url",
    is_flag=True,
    show_default=True,
    help="Always use direct URL to point to distributions.",
)
@click.option(
    "--version",
    is_flag=True,
    help="Print version and exit.",
)
def cli(site_packages: str, debug: bool, ignore_errors: bool, direct_url: bool, version: str) -> None:
    """Reconstruct requirements from site-packages."""
    from ._lib import preserve_requirements
    from pip_preserve import __title__
    from pip_preserve import __version__

    if version:
        click.echo(f"{__title__}: {__version__}")
        sys.exit(0)

    if debug:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("%s in version %s", __title__, __version__)

    site_packages_listing = site_packages.split(os.pathsep)

    requirements = preserve_requirements(
        site_packages_listing,
        ignore_errors=ignore_errors,
        direct_url=direct_url
    )
    if requirements is None:
        sys.exit(1)

    click.echo(requirements)


__name__ == "__main__" and cli()
