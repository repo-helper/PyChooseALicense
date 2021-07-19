# stdlib
import os

# 3rd party
import pytest
from coincidence.params import param
from domdf_python_tools.paths import PathPlus

# this package
from pychoosealicense import detect

example_licenses_dir = PathPlus(__file__).parent / "example_licenses"

# TODO: more


@pytest.mark.parametrize(
		"filename, identifier",
		[
				param("BSD2_1", "BSD-2-Clause", idx=0),
				param("BSD2_2", "BSD-2-Clause", idx=0),
				param("BSD2_3", "BSD-2-Clause", idx=0),
				param("MIT_1", "MIT", idx=0),
				param("MIT_2", "MIT", idx=0),
				param("WTFPL_1", "WTFPL", idx=0),
				]
		)
def test_detect(filename: str, identifier: str):
	content = (example_licenses_dir / filename).read_text()
	the_license = detect.detect(content)
	assert the_license is not None
	assert the_license.spdx_id == identifier


@pytest.mark.parametrize(
		"filename, identifier",
		[
				param("BSD2_1", "BSD-2-Clause", idx=0),
				param("BSD2_2", "BSD-2-Clause", idx=0),
				param("BSD2_3", "BSD-2-Clause", idx=0),
				param("MIT_1", "MIT", idx=0),
				param("MIT_2", "MIT", idx=0),
				param("WTFPL_1", "WTFPL", idx=0),
				]
		)
def test_detect_file(filename: str, identifier: str):
	the_license = detect.detect_file(example_licenses_dir / filename)
	assert the_license is not None
	assert the_license.spdx_id == identifier

	the_license = detect.detect_file(str(example_licenses_dir / filename))
	assert the_license is not None
	assert the_license.spdx_id == identifier


def test_license_not_identified():
	assert detect.detect_file(os.devnull) is None
