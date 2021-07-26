#!/usr/bin/env python3
#
#  __init__.py
"""
Provides license metadata from `choosealicense.com`_.

.. _choosealicense.com: https://choosealicense.com
.. _popular: https://opensource.org/licenses
.. _spectrum of licenses: https://choosealicense.com/licenses/
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
import functools
import re
from typing import NamedTuple, Optional, Tuple

# 3rd party
import frontmatter  # type: ignore
from domdf_python_tools.compat import importlib_resources

# this package
from pychoosealicense import rules

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2021 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["License", "get_license"]

_yaml_handler = frontmatter.YAMLHandler()
_field_convert_re = re.compile(r"\[(fullname|login|email|project|description|year|projecturl)]")
_brace_map = {ord('{'): "{{", ord('}'): "}}"}


class License(NamedTuple):
	"""
	Represents a license, with its text and associated metadata.

	.. versionchanged:: 0.2.0

		``conditions``, ``permissions`` and ``limitations`` are now :class:`tuples <tuple>`
		rather than :class:`lists <list>` to maintain immutability of the :class:`~.License` object.
	"""

	#: The license full name specified by https://spdx.org/licenses/
	title: str

	#: Short identifier specified by https://spdx.org/licenses/
	spdx_id: str

	#: A human-readable description of the license.
	description: str

	#: Instructions on how to implement the license.
	how: str

	#: Bulleted list of required rules.
	conditions: Tuple["rules.Rule", ...]

	#: Bulleted list of permitted rules.
	permissions: Tuple["rules.Rule", ...]

	#: Bulleted list of limited rules.
	limitations: Tuple["rules.Rule", ...]

	#: The text of the license.
	content: str

	#: Whether the license is be featured on the choosealicense.com main page.
	featured: bool = False

	hidden: bool = True
	"""
	Whether the license is neither `popular`_ nor fills out the `spectrum of licenses`_
	from strongly conditional to unconditional.
	"""

	#: Customary short name if applicable (e.g, GPLv3)
	nickname: Optional[str] = None

	#: Additional information about the licenses
	note: Optional[str] = None

	def __repr__(self) -> str:
		"""
		Return a string representation of the :class:`~.License`.
		"""

		return f"<{self.__class__.__name__}(title={self.title!r}, spdx_id={self.spdx_id!r})>"


@functools.lru_cache()
def get_license(identifier: str) -> License:
	"""
	Return the license text and metadata for the given identifier.

	:param identifier:
	"""

	license_file = f"{identifier.lower()}.txt".replace(' ', '-')

	try:
		content = importlib_resources.read_text("pychoosealicense._licenses", license_file)
	except FileNotFoundError:
		raise ValueError(f"Unknown license identifier {identifier!r}") from None

	content = content.replace("\r\n", '\n').translate(_brace_map)
	metadata, content = frontmatter.parse(content, handler=_yaml_handler)

	# convert and remove fields
	if "spdx-id" in metadata:
		metadata["spdx_id"] = metadata.pop("spdx-id")
	if "using" in metadata:
		del metadata["using"]
	if "redirect_from" in metadata:
		del metadata["redirect_from"]

	metadata["conditions"] = tuple(map(rules.rules["conditions"].__getitem__, metadata["conditions"]))
	metadata["permissions"] = tuple(map(rules.rules["permissions"].__getitem__, metadata["permissions"]))
	metadata["limitations"] = tuple(map(rules.rules["limitations"].__getitem__, metadata["limitations"]))

	# convert fields to curly-brace format strings
	content = _field_convert_re.sub(r"{\1}", content)
	metadata["how"] = _field_convert_re.sub(r"{\1}", metadata["how"].translate(_brace_map))

	return License(**metadata, content=content)
