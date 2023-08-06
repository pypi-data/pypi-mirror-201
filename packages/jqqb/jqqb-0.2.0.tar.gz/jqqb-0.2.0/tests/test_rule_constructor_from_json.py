import unittest

from jqqb.aggregator import AllAggregator, AnyAggregator
from jqqb.boolean_operation import BooleanOperation
from jqqb.rule_connective import RuleConnective
from jqqb.rule_constructor_from_json import RuleConstructorFromJson


class TestCreateAggregatorFromJson(unittest.TestCase):
    def setUp(self) -> None:
        self.RULE_CONSTRUCTOR_FROM_JSON = RuleConstructorFromJson()
        self.instance_json = {
            # "aggregator" field to set in test
            "field": "dummy_aggregate_field",
            "rule": {
                "inputs": [
                    {
                        "field": "dummy_boolean_operation_field",
                        "type": "boolean"
                    },
                    {"type": "boolean", "value": True},
                ],
                "operator": "equal",
            }
        }
        return super().setUp()

    def test_create_all_aggregator_from_json_using_all_aggregator_constructor(
        self,
    ):
        self.instance_json["aggregator"] = "ALL"
        instance = self.RULE_CONSTRUCTOR_FROM_JSON.create_aggregator_from_json(
            json_entry=self.instance_json
        )

        self.assertIsInstance(instance, AllAggregator)

    def test_create_all_aggregator_from_json_using_rule_constructor(self):
        self.instance_json["aggregator"] = "ALL"
        instance = self.RULE_CONSTRUCTOR_FROM_JSON.create_rule_from_json(
            json_entry=self.instance_json
        )

        self.assertIsInstance(instance, AllAggregator)

    def test_create_any_aggregator_from_json_using_any_aggregator_constructor(
        self,
    ):
        self.instance_json["aggregator"] = "ANY"
        instance = self.RULE_CONSTRUCTOR_FROM_JSON.create_aggregator_from_json(
            json_entry=self.instance_json
        )

        self.assertIsInstance(instance, AnyAggregator)

    def test_create_any_aggregator_from_json_using_rule_constructor(self):
        self.instance_json["aggregator"] = "ANY"
        instance = self.RULE_CONSTRUCTOR_FROM_JSON.create_rule_from_json(
            json_entry=self.instance_json
        )

        self.assertIsInstance(instance, AnyAggregator)


class TestCreateBooleanOperationFromJson(unittest.TestCase):
    def setUp(self) -> None:
        self.RULE_CONSTRUCTOR_FROM_JSON = RuleConstructorFromJson()
        self.instance_json = {
            "operator": "equal",
            "inputs": [
                {"field": "dummy_key", "type": "str"},
                {"value": "dummy_value", "type": "str"},
            ],
        }
        return super().setUp()

    def test_create_boolean_operation_from_json_using_boolean_operation_constructor(
        self,
    ):
        instance = self.RULE_CONSTRUCTOR_FROM_JSON.create_boolean_operation_from_json(
            json_entry=self.instance_json
        )

        self.assertIsInstance(instance, BooleanOperation)

    def test_create_all_aggregator_from_json_using_rule_constructor(self):
        instance = self.RULE_CONSTRUCTOR_FROM_JSON.create_rule_from_json(
            json_entry=self.instance_json
        )

        self.assertIsInstance(instance, BooleanOperation)


class TestCreateRuleConnectiveFromJson(unittest.TestCase):
    def setUp(self) -> None:
        self.RULE_CONSTRUCTOR_FROM_JSON = RuleConstructorFromJson()
        self.instance_json = {
            "condition": "AND",
            "rules": [{
                "operator": "equal",
                "inputs": [
                    {"field": "dummy_key", "type": "str"},
                    {"value": "dummy_value", "type": "str"},
                ],
            }],
        }
        return super().setUp()

    def test_create_rule_connective_from_json_using_rule_connective_constructor(
        self,
    ):
        instance = self.RULE_CONSTRUCTOR_FROM_JSON.create_rule_connective_from_json(
            json_entry=self.instance_json
        )

        self.assertIsInstance(instance, RuleConnective)

    def test_create_all_aggregator_from_json_using_rule_constructor(self):
        instance = self.RULE_CONSTRUCTOR_FROM_JSON.create_rule_from_json(
            json_entry=self.instance_json
        )

        self.assertIsInstance(instance, RuleConnective)
