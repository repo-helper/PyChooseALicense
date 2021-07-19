# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture, AdvancedFileRegressionFixture

# this package
from pychoosealicense import License, get_license


def test_get_license(
		identifier: str,
		advanced_file_regression: AdvancedFileRegressionFixture,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	the_license = get_license(identifier)
	assert isinstance(the_license, License)

	advanced_data_regression.check(the_license)

	metadata = {
			"fullname": "Dominic Davis-Foster",
			"login": "domdfcoding",
			"email": "dominic@davis-foster.co.uk",
			"project": "pychoosealicense",
			"description": "Provides license metadata from choosealicense.com",
			"year": 2021,
			"projecturl": "https://github.com/repo-helper/pychoosealicense",
			}
	advanced_file_regression.check(
			the_license.content.format(**metadata),
			extension=".md",
			)
	advanced_file_regression.check(
			the_license.content.format_map(metadata),
			extension=".md",
			)


@pytest.mark.parametrize("identifier", ["BSD0", "GPLv3", "X11"])
def test_unknown_identifier(identifier: str):
	with pytest.raises(ValueError, match="Unknown license identifier '"):
		get_license(identifier)
