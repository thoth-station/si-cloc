#!/usr/bin/env python3
# si-cloc
# Copyright(C) 2020 Kevin Postlethwait.
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This is the main script of si-cloc which counts lines of code."""

import tempfile
import click
import os
import logging
from typing import Optional
from thoth.analyzer import run_command
from thoth.analyzer import print_command_result
from thoth.common import init_logging
from thoth.analyzer import __version__ as __analyzer__version__
from thoth.common import __version__ as __common__version__

init_logging()

__version__ = "0.1.3"
__title__ = "si-cloc"

__component_version__ = f"{__version__}+" f"analyzer.{__analyzer__version__}.common.{__common__version__}."

_LOGGER = logging.getLogger(__title__)
_LOGGER.info("SI Cloc v%s", __component_version__)


@click.command()
@click.pass_context
@click.option(
    "--output", "-o", type=str, default="-", envvar="THOTH_SI_CLOC_OUTPUT", help="Output file to print results to."
)
@click.option(
    "--from-directory", "-d", type=str, envvar="THOTH_SI_CLOC_DIR", help="Input directory for running bandit."
)
@click.option(
    "--package-name",
    "-n",
    required=True,
    type=str,
    envvar="THOTH_SI_CLOC_PACKAGE_NAME",
    help="Name of package bandit is being run on.",
)
@click.option(
    "--package-version",
    type=str,
    required=True,
    envvar="THOTH_SI_CLOC_PACKAGE_VERSION",
    help="Version to be evaluated.",
)
@click.option(
    "--package-index",
    type=str,
    default="https://pypi.org/simple",
    envvar="THOTH_SI_CLOC_PACKAGE_INDEX",
    help="Which index is used to find package.",
)
@click.option("--no-pretty", is_flag=True, help="Do not print results nicely.")
def si_cloc(
    click_ctx,
    output: Optional[str],
    from_directory: Optional[str],
    package_name: str,
    package_version: Optional[str],
    package_index: Optional[str],
    no_pretty: bool,
):
    """Run the cli for si-cloc."""
    if from_directory is None:
        with tempfile.TemporaryDirectory() as d:
            command = (
                f"pip download --no-binary=:all: --no-deps -d {d} -i {package_index} "
                f"{package_name}==={package_version}"
            )
            run_command(command)
            for f in os.listdir(d):
                if f.endswith(".tar.gz"):
                    full_path = os.path.join(d, f)
                    break
            else:
                raise FileNotFoundError(
                    f"No source distribution found for {package_name}==={package_version} " f"on {package_index}"
                )

            out = run_command(f"cloc --extract-with='gzip -dc >FILE< | tar xf -' {full_path} --json", is_json=True)
    else:
        out = run_command(f"cloc {from_directory} --json", is_json=True)
    results = out.stdout
    if results is None:
        results = {"error": True, "error_messages": [out.stderr]}
        _LOGGER.warning("cloc output is empty with the following in stderr:\n%s", out.stderr)
    else:
        results["error"] = False

    print_command_result(
        click_ctx=click_ctx,
        result=results,
        analyzer=__title__,
        analyzer_version=__version__,
        output=output,
        duration=None,
        pretty=not no_pretty,
    )


__name__ == "__main__" and si_cloc()
