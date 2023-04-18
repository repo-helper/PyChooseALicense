# 3rd party
import pytest

pytest_plugins = ("coincidence", "consolekit.testing")


@pytest.fixture(
		params=[
				pytest.param("MIT", id="mit_upper"),
				pytest.param("mit", id="mit_lower"),
				pytest.param("mIt", id="mit_mixed"),
				pytest.param("0bsd", id="0bsd_lower"),
				pytest.param("0BSD", id="0bsd_upper"),
				pytest.param("bsd 2 clause", id="bsd_2_lower"),
				pytest.param("BSD 2-Clause", id="bsd_2_upper"),
				pytest.param("BSD 3 Clause", id="bsd_3_upper"),
				pytest.param("bsd-3-clause", id="bsd_3_lower"),
				pytest.param("afl-3.0", id="afl-3.0"),
				pytest.param("agpl-3.0", id="agpl-3.0"),
				pytest.param("Apache 2.0", id="apache-2.0"),
				pytest.param("artistic 2.0", id="artistic-2.0"),
				pytest.param("bsl-1.0", id="bsl-1.0"),
				pytest.param("cc0-1.0", id="cc0-1.0"),
				pytest.param("ecl-2.0", id="ecl-2.0"),
				pytest.param("epl-1.0", id="epl-1.0"),
				pytest.param("epl-2.0", id="epl-2.0"),
				pytest.param("eupl-1.1", id="eupl-1.1"),
				pytest.param("eupl-1.2", id="eupl-1.2"),
				pytest.param("cc-by-sa-4.0", id="cc-by-sa-4.0_lower"),
				pytest.param("CC BY SA 4.0", id="cc-by-sa-4.0_upper"),
				pytest.param("cc-by 4.0", id="cc-by-4.0_lower"),
				pytest.param("CC-BY-4.0", id="cc-by-4.0_upper"),
				pytest.param("gpl-2.0", id="gpl-2.0_lower"),
				pytest.param("GPL 2.0", id="gpl-2.0_upper"),
				pytest.param("gpl 3.0", id="gpl-3.0_lower"),
				pytest.param("GPL-3.0", id="gpl-3.0_upper"),
				pytest.param("gpl-2.0 only", id="gpl-2.0 only_lower"),
				pytest.param("GPL 2.0-only", id="gpl-2.0-only_upper"),
				pytest.param("GPL-3.0-only", id="gpl-3.0-only_upper"),
				pytest.param("lgpl 2.1", id="lgpl-2.1_lower"),
				pytest.param("LGPL-2.1", id="lgpl-2.1_upper"),
				pytest.param("lgpl-3.0", id="lgpl-3.0_lower"),
				pytest.param("LGPL 3.0", id="lgpl-3.0_upper"),
				pytest.param("unlicense", id="unlicense"),
				]
		)
def identifier(request) -> str:
	return request.param
