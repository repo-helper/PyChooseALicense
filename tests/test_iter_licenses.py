# stdlib
from typing import Iterator

# 3rd party
from coincidence import AdvancedDataRegressionFixture

# this package
from pychoosealicense import License, iter_licenses


def test_iter_licenses(advanced_data_regression: AdvancedDataRegressionFixture):
	licenses = iter_licenses()
	assert isinstance(licenses, Iterator)

	first_license = next(licenses)
	assert isinstance(first_license, License)
	identifiers = {first_license.spdx_id}

	second_license = next(licenses)
	assert isinstance(second_license, License)
	identifiers.add(second_license.spdx_id)

	for license in licenses:
		identifiers.add(license.spdx_id)

	advanced_data_regression.check(sorted(identifiers))
