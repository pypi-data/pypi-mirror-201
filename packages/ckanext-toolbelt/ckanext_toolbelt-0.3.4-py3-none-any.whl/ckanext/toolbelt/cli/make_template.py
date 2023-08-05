from __future__ import annotations

from typing import Optional

import click

from . import _shared

option_file = click.option(
    "-f",
    "--file",
    help=("Append output to the specified file instead of printing to STDOUT"),
)


@click.group()
# @click.argument(
#     "template", type=click.Choice(["black", "isort", "pyright", "pytest", "ruff"])
# )
def template():
    """Print fragments that are used by other make commands."""


@template.command()
@_shared.option_plugin
@option_file
def black(plugin: str, file: Optional[str]):
    """Black configuration"""
    _shared.ensure_root()
    _shared.produce(
        _shared.template_source("black"),
        file or "",
        {"PLUGIN": _shared.safe_plugin_name(plugin)},
        bool(file),
    )


@template.command()
@_shared.option_plugin
@option_file
def isort(plugin: str, file: Optional[str]):
    """Isort configuration"""
    _shared.ensure_root()
    _shared.produce(
        _shared.template_source("isort"),
        file or "",
        {"PLUGIN": _shared.safe_plugin_name(plugin)},
        bool(file),
    )


@template.command()
@_shared.option_plugin
@option_file
def ruff(plugin: str, file: Optional[str]):
    """Ruff configuration"""
    _shared.ensure_root()
    _shared.produce(
        _shared.template_source("ruff"),
        file or "",
        {"PLUGIN": _shared.safe_plugin_name(plugin)},
        bool(file),
    )


@template.command()
@_shared.option_plugin
@option_file
def pyright(plugin: str, file: Optional[str]):
    """Pyrigh configuration"""
    _shared.ensure_root()
    _shared.produce(
        _shared.template_source("pyright"),
        file or "",
        {"PLUGIN": _shared.safe_plugin_name(plugin)},
        bool(file),
    )


@template.command()
@_shared.option_plugin
@option_file
def pytest(plugin: str, file: Optional[str]):
    """Pytest configuration"""
    _shared.ensure_root()
    _shared.produce(
        _shared.template_source("pytest"),
        file or "",
        {"PLUGIN": _shared.safe_plugin_name(plugin)},
        bool(file),
    )


@template.command()
@_shared.option_plugin
@option_file
def commitizen(plugin: str, file: Optional[str]):
    """Commitizen configuration"""
    _shared.ensure_root()
    _shared.produce(
        _shared.template_source("commitizen"),
        file or "",
        {"PLUGIN": _shared.safe_plugin_name(plugin)},
        bool(file),
    )
