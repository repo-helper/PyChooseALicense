#!/usr/bin/env python3
#
#  description.py
"""
Functions for converting a license's description to HTML, Markdown etc.

.. versionadded:: 0.2.0
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
import re
from typing import Match
from urllib.parse import urlparse, urlunparse

__all__ = ["as_html", "as_markdown", "as_plaintext", "as_rst"]

_a_tag_re = re.compile(r'<a href=(["\'])(?P<href>.*?)\1>(?P<title>.*?)</a>')


def _substitute_netloc(href: str) -> str:

	if not re.match("([A-Za-z-.]+:)?//", href):
		href = "//" + str(href)

	scheme, netloc, parts, params, query, fragment = urlparse(href)

	if not netloc:
		netloc = "choosealicense.com"
		scheme = "https"

	return urlunparse([scheme, netloc, parts, params, query, fragment])


def _anchor_replacement_html(match: Match) -> str:
	groups = match.groupdict()
	href = _substitute_netloc(groups["href"])
	return f"<a href='{href}'>{groups['title']}</a>"


def _anchor_replacement_rst(match: Match) -> str:
	groups = match.groupdict()
	href = _substitute_netloc(groups["href"])
	return f"`{groups['title']} <{href}>`_"


def _anchor_replacement_markdown(match: Match) -> str:
	groups = match.groupdict()
	href = _substitute_netloc(groups["href"])
	return f"[{groups['title']}]({href})"


def _anchor_replacement_plaintext(match: Match) -> str:
	return match.groupdict()["title"]


def as_html(description: str) -> str:
	"""
	Returns the description as an HTML string.

	:param description:
	"""

	return _a_tag_re.sub(_anchor_replacement_html, description)


def as_rst(description: str) -> str:
	"""
	Returns the description as a reStructuredText string.

	:param description:
	"""

	return _a_tag_re.sub(_anchor_replacement_rst, description)


def as_markdown(description: str) -> str:
	"""
	Returns the description as a Markdown string.

	:param description:
	"""

	return _a_tag_re.sub(_anchor_replacement_markdown, description)


def as_plaintext(description: str) -> str:
	"""
	Returns the description as a plaintext string.

	:param description:
	"""

	return _a_tag_re.sub(_anchor_replacement_plaintext, description)
