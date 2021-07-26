#!/usr/bin/env python3
#
#  __main__.py
"""
CLI entry point.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import sys
from typing import TYPE_CHECKING

# 3rd party
import click  # nodep
from consolekit import click_command  # nodep
from consolekit.options import colour_option, verbose_option  # nodep

if TYPE_CHECKING:
	# 3rd party
	from consolekit.terminal_colours import ColourTrilean

__all__ = ["main"]


@verbose_option(help_text="Show a description of each rule (permission, limitation etc.)")
@colour_option()
@click.argument("license")
@click_command()
def main(
		license: str,  # noqa: A002  # pylint: disable=redefined-builtin
		colour: "ColourTrilean" = None,
		verbose: bool = False,
		):
	"""
	Show information about the given license.
	"""

	# this package
	from pychoosealicense._cli import CLI

	cli = CLI(license, colour)
	cli.print_info(verbose)


if __name__ == "__main__":
	sys.exit(main())
