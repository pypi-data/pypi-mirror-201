import unittest

from jqqb.boolean_operation import BooleanOperation
from jqqb.input import Input
from jqqb.operator import Operator
from jqqb.rule_connective import RuleConnective


class TestRuleConnectiveJsonify(unittest.TestCase):
    def setUp(self) -> None:
        self.object = {"dummy_key": "dummy_value"}
        self.expected_result = {
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

    def test_rule_connective_jsonify(self):
        instance = RuleConnective(
            condition="AND",
            rules=[
                BooleanOperation(
                    operator=Operator.eval_equal,
                    inputs=[
                        Input(type="str", field="dummy_key"),
                        Input(type="str", value="dummy_value"),
                    ],
                ),
            ],
        )
        result = instance.jsonify(object=self.object)

        self.assertEqual(result, self.expected_result)


class TestEvaluateAndRuleConnective(unittest.TestCase):
    def setUp(self) -> None:
        self.rule_connective = RuleConnective(
            condition="AND",
            rules=[
                BooleanOperation(
                    operator=Operator.eval_equal,
                    inputs=[
                        Input(type="str", field="dummy_key"),
                        Input(type="str", value="dummy_value"),
                    ],
                ),
                BooleanOperation(
                    operator=Operator.eval_not_equal,
                    inputs=[
                        Input(type="str", field="dummy_key"),
                        Input(type="str", value="dummy_value"),
                    ],
                )
            ]
        )
        self.object = {"dummy_key": "dummy_value"}
        return super().setUp()
    
    def test_evaluate_any_aggregator(self):
        result = self.rule_connective.evaluate(object=self.object)

        self.assertFalse(result)


class TestEvaluateOrRuleConnective(unittest.TestCase):
    def setUp(self) -> None:
        self.rule_connective = RuleConnective(
            condition="OR",
            rules=[
                BooleanOperation(
                    operator=Operator.eval_equal,
                    inputs=[
                        Input(type="str", field="dummy_key"),
                        Input(type="str", value="dummy_value"),
                    ],
                ),
                BooleanOperation(
                    operator=Operator.eval_not_equal,
                    inputs=[
                        Input(type="str", field="dummy_key"),
                        Input(type="str", value="dummy_value"),
                    ],
                )
            ]
        )
        self.object = {"dummy_key": "dummy_value"}
        return super().setUp()
    
    def test_evaluate_any_aggregator(self):
        result = self.rule_connective.evaluate(object=self.object)

        self.assertTrue(result)
