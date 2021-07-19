# 3rd party
from coincidence import AdvancedDataRegressionFixture

# this package
from pychoosealicense.rules import Rule, _get_rules, rules


def test_rule():
	r = Rule(
			tag="my-rule",
			label="My Rule",
			description="This is the description of my rule. Here you can explain the rule in more detail.",
			)
	assert r.tag == "my-rule"
	assert r.label == "My Rule"
	assert r.description == "This is the description of my rule. Here you can explain the rule in more detail."

	assert r._asdict() == dict(
			tag="my-rule",
			label="My Rule",
			description="This is the description of my rule. Here you can explain the rule in more detail.",
			)


class TestGetRules:

	def test_rules(self, advanced_data_regression: AdvancedDataRegressionFixture):
		the_rules = _get_rules.__wrapped__()
		assert isinstance(the_rules, dict)
		assert list(the_rules.keys()) == ["permissions", "conditions", "limitations"]
		assert isinstance(the_rules["permissions"], dict)
		assert isinstance(the_rules["conditions"], dict)
		assert isinstance(the_rules["limitations"], dict)

		advanced_data_regression.check(the_rules)

	def test_cache(self):
		assert _get_rules() == _get_rules()
		assert _get_rules() is _get_rules()

		assert _get_rules() == rules
		assert _get_rules() is rules


class TestRulesObject:

	def test_rules(self, advanced_data_regression: AdvancedDataRegressionFixture):
		assert isinstance(rules, dict)
		assert list(rules.keys()) == ["permissions", "conditions", "limitations"]
		assert isinstance(rules["permissions"], dict)
		assert isinstance(rules["conditions"], dict)
		assert isinstance(rules["limitations"], dict)

		advanced_data_regression.check(rules)
