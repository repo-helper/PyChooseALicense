# stdlib
from operator import attrgetter

# this package
from pychoosealicense import License, get_license


def test_license_class():
	text = (
			"This software may only be obtained by sending the author a postcard, "
			"and then the user promises not to redistribute it."
			)
	how = f"At the top of each file write {text!r}"

	l = License(
			"Dom's License",
			"dom-1.0",
			description="A license I just made up.",
			how=how,
			conditions=[],
			permissions=[],
			limitations=[],
			content=text,
			hidden=False,
			nickname="DomLicense",
			note="This license is fictitious.",
			)

	assert l.title == "Dom's License"
	assert l.spdx_id == "dom-1.0"
	assert l.description == "A license I just made up."
	assert l.how == how
	assert l.conditions == []
	assert l.permissions == []
	assert l.limitations == []
	assert l.content == text
	assert l.featured is False
	assert l.hidden is False
	assert l.nickname == "DomLicense"
	assert l.note == "This license is fictitious."

	assert repr(l) == "<License(title=\"Dom's License\", spdx_id='dom-1.0')>"


def test_license_class_mit():
	mit_license = get_license("MIT")

	assert mit_license.title == "MIT License"
	assert mit_license.spdx_id == "MIT"
	assert mit_license.featured is True
	assert mit_license.hidden is False

	assert mit_license.description == (
			"A short and simple permissive license with conditions only "
			"requiring preservation of copyright and license notices. "
			"Licensed works, modifications, and larger works may be distributed "
			"under different terms and without source code."
			)

	assert mit_license.how == (
			"Create a text file (typically named LICENSE or LICENSE.txt) "
			"in the root of your source code and copy the text of the license "
			"into the file. Replace {year} with the current year and {fullname} "
			"with the name (or names) of the copyright holders."
			)

	assert list(map(attrgetter("tag"), mit_license.permissions)) == [
			"commercial-use",
			"modifications",
			"distribution",
			"private-use",
			]
	assert list(map(attrgetter("tag"), mit_license.conditions)) == ["include-copyright"]
	assert list(map(attrgetter("tag"), mit_license.limitations)) == ["liability", "warranty"]
