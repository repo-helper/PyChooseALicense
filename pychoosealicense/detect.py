#!/usr/bin/env python3
#
#  detect.py
"""
Functions for detecting licenses from files.

.. versionadded:: 0.3.0

.. extras-require:: detect
	:pyproject:


The prodecure is roughly as follows:

1. Remove copyright line(s).
2. Normalize whitespace (replace all whitespace with a single space).
3. Check for an exact text match with the supported licenses.
4. Failing that, check the edit distance against the supported licenses.
"""
#
#  Copyright © 2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on https://github.com/pre-commit/identify
#  Copyright (c) 2017 Chris Kuehl, Anthony Sottile
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
import os
import pathlib
import re
import sys
from typing import Optional, Union

# 3rd party
import editdistance_s  # type: ignore  # nodep

# this package
from pychoosealicense import License, iter_licenses

__all__ = ["detect", "detect_file"]

COPYRIGHT_RE = re.compile(r'^\s*(Copyright|\(C\)) .*$', re.I | re.MULTILINE)
WS_RE = re.compile(r'\s+')


def detect(license_text: str) -> Optional[License]:
	"""
	Returns the :class:`~.License` object for the given license text.

	If no license is detected, returns :py:obj:`None`.

	:param license_text:
	"""

	norm = COPYRIGHT_RE.sub('', license_text)
	norm = WS_RE.sub(' ', norm).strip()

	min_edit_dist = sys.maxsize
	min_edit_dist_license: Optional[License] = None

	# try exact matches
	for candidate in iter_licenses():
		norm_license = COPYRIGHT_RE.sub('', candidate.content)
		norm_license = WS_RE.sub(' ', norm_license).strip()
		if norm == norm_license:
			return candidate

		# skip the slow calculation if the lengths are very different
		if norm and abs(len(norm) - len(norm_license)) / len(norm) > .05:
			continue

		edit_dist = editdistance_s.distance(norm, norm_license)
		if edit_dist < min_edit_dist:
			min_edit_dist = edit_dist
			min_edit_dist_license = candidate

	# if there's less than 5% edited from the license, we found our match
	if norm and min_edit_dist / len(norm) < .05:
		return min_edit_dist_license
	else:
		# no matches :'(
		return None


def detect_file(filename: Union[str, pathlib.Path, os.PathLike]) -> Optional[License]:
	"""
	Returns the :class:`~.License` object for the license contained in ``filename``.

	If no license is detected, returns :py:obj:`None`.

	:param filename:
	"""

	with open(filename, encoding="UTF-8") as fp:
		return detect(fp.read())
