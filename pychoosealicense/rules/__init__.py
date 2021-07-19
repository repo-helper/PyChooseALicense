#!/usr/bin/env python3
#
#  __init__.py
"""
Models conditions, permissions and limitations attached to licenses.
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
from typing import Dict, NamedTuple

# 3rd party
import frontmatter  # type: ignore
import importlib_resources
import yaml
from typing_extensions import TypedDict

__all__ = ["Rule", "RuleMap", "rules"]


class Rule(NamedTuple):
	"""
	Represents a permission, condition or limitation attached to a license.
	"""

	#: An identifier for the rule, e.g. ``'commercial-use'``.
	tag: str

	#: A short label, e.g. ``'Commercial use'``.
	label: str

	#: A short description of the rule.
	description: str


class RuleMap(TypedDict):
	"""
	Represents a mapping of rule types to mappings of rule tags to individual rules.
	"""

	permissions: Dict[str, Rule]
	conditions: Dict[str, Rule]
	limitations: Dict[str, Rule]


@functools.lru_cache(1)
def _get_rules() -> RuleMap:
	with importlib_resources.open_text("pychoosealicense.rules", "rules.yml") as fp:
		raw_rules = yaml.safe_load(fp)

	data: RuleMap = {"permissions": {}, "conditions": {}, "limitations": {}}

	for rule in raw_rules["permissions"]:
		data["permissions"][rule["tag"]] = Rule(**rule)

	for rule in raw_rules["conditions"]:
		data["conditions"][rule["tag"]] = Rule(**rule)

	for rule in raw_rules["limitations"]:
		data["limitations"][rule["tag"]] = Rule(**rule)

	return data


#: The currently supported rules, grouped by type.
rules: RuleMap = _get_rules()
