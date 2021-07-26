#!/usr/bin/env python3
#
#  _cli.py
"""
Internal CLI helpers.
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
import shutil
import textwrap
from functools import partial
from itertools import zip_longest

# 3rd party
import click  # nodep
from consolekit.terminal_colours import ColourTrilean, Fore, Style, resolve_color_default  # nodep

# this package
from pychoosealicense import description, get_license
from pychoosealicense.rules import Rule

__all__ = ["CLI"]


class CLI:
	"""
	Helper for printing information about a license.

	:param license_key: The SPDX identifier of the license.
	:param colour: Whether to force coloured output on or off.
	"""

	def __init__(self, license_key: str, colour: ColourTrilean = None):
		self.the_license = get_license(license_key)
		self.colour = resolve_color_default(colour)
		self.term_size = min(shutil.get_terminal_size().columns, 120)
		self._echo = partial(click.echo, color=resolve_color_default(colour))

	def _serial_rules(self) -> None:

		self._echo(Fore.GREEN("Permissions"))
		for permission in self.the_license.permissions:
			self._echo(permission.label)
		self._echo()

		self._echo(Fore.BLUE("Conditions"))
		for condition in self.the_license.conditions:
			self._echo(condition.label)
		self._echo()

		self._echo(Fore.RED("Limitations"))
		for limitation in self.the_license.limitations:
			self._echo(limitation.label)
		self._echo()

	def _verbose_rules(self) -> None:
		# TODO: handle really narrow terminals (less than longest label)
		#  Perhaps put description in wrapped paragraph on the next line

		indent = 4

		def print_rule(rule: Rule):
			label = f"{rule.label} \u2013 "
			max_desc_width = self.term_size - indent
			first_line_extra_indent = (len(label) - indent) * ' '
			wrapped_description = textwrap.wrap(first_line_extra_indent + rule.description, width=max_desc_width)
			self._echo(f"{label}{wrapped_description[0].lstrip()}")
			for line in wrapped_description[1:]:
				self._echo(f"{' ' * indent}{line}")

		self._echo(Fore.GREEN("Permissions"))
		for permission in self.the_license.permissions:
			print_rule(permission)

		self._echo()

		self._echo(Fore.BLUE("Conditions"))
		for condition in self.the_license.conditions:
			print_rule(condition)

		self._echo()

		self._echo(Fore.RED("Limitations"))
		for limitation in self.the_license.limitations:
			print_rule(limitation)

		self._echo()

	def print_rule_table(self, verbose: bool = False) -> None:
		"""
		Print a table of the permissions, conditions and limitations associated with the license.

		:param verbose: Whether to show a description of each rule (permission, limitation etc.)
		"""

		if verbose:
			return self._verbose_rules()

		data = [
				self.the_license.permissions,
				self.the_license.conditions,
				self.the_license.limitations,
				]

		def get_rule_length(rule: Rule):
			return len(rule.label) + 2

		rule_lengths = (tuple(map(get_rule_length, row)) for row in data)
		min_col_widths = []

		for row, label_width in zip(rule_lengths, (12, 11, 12)):
			if row:
				min_col_widths.append(max(max(row), label_width))
			else:
				min_col_widths.append(label_width)

		if sum(min_col_widths) > self.term_size:
			return self._serial_rules()

		scale = self.term_size / sum(min_col_widths)
		column_widths = [int(w * scale) for w in min_col_widths]

		self._echo(Fore.GREEN("Permissions"), nl=False)
		self._echo(' ' * (column_widths[0] - 11), nl=False)
		self._echo(Fore.BLUE("Conditions"), nl=False)
		self._echo(' ' * (column_widths[1] - 10), nl=False)
		self._echo(Fore.RED("Limitations"))

		_empty_rule = Rule('', '', '')

		for permission, condition, limitation in zip_longest(*data, fillvalue=_empty_rule):
			self._echo(permission.label, nl=False)
			self._echo(' ' * (column_widths[0] - len(permission.label)), nl=False)
			self._echo(condition.label, nl=False)
			self._echo(' ' * (column_widths[1] - len(condition.label)), nl=False)
			self._echo(limitation.label)

		self._echo()

	def print_header(self):
		"""
		Print a header giving the name of the license and a short description.
		"""

		self._echo(Style.BRIGHT(self.the_license.title))
		self._echo(Style.BRIGHT('=' * len(self.the_license.title)))
		self._echo()

		the_description = description.as_plaintext(self.the_license.description)
		self._echo('\n'.join(textwrap.wrap(the_description, width=self.term_size)))
		self._echo()

	def print_info(self, verbose: bool = False):
		"""
		Print information about the license.

		:param verbose: Whether to show a description of each rule (permission, limitation etc.)
		"""

		self.print_header()
		self.print_rule_table(verbose=verbose)
