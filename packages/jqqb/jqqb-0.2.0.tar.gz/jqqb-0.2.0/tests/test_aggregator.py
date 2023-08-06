import unittest

from jqqb.aggregator import Aggregator, AnyAggregator, AllAggregator
from jqqb.boolean_operation import BooleanOperation
from jqqb.input import Input
from jqqb.operator import Operator


class TestCreateAggregator(unittest.TestCase):
    def setUp(self) -> None:
        self.rule = BooleanOperation(
            inputs=[
                Input(field="dummy_boolean_operation_field", type="boolean"),
                Input(type="boolean", value=True),
            ],
            operator=Operator.eval_equal,
        )
        return super().setUp()

    def test_create_all_aggregator_from_Aggregator_facade(self):
        instance = Aggregator(
            aggregator="ALL", field="dummy_aggregate_field", rule=self.rule
        )

        self.assertIsInstance(instance, AllAggregator)

    def test_create_any_aggregator_from_Aggregator_facade(self):
        instance = Aggregator(
            aggregator="ANY", field="dummy_aggregate_field", rule=self.rule
        )

        self.assertIsInstance(instance, AnyAggregator)


class TestJsonifyAllAggregator(unittest.TestCase):
    def setUp(self) -> None:
        self.aggregator = Aggregator(
            aggregator="ALL",
            field="dummy_aggregate_field",
            rule=BooleanOperation(
                inputs=[
                    Input(
                        field="dummy_boolean_operation_field", type="boolean"
                    ),
                    Input(type="boolean", value=True),
                ],
                operator=Operator.eval_equal,
            )
        )
        self.object = {
            "dummy_aggregate_field": [{"dummy_boolean_operation_field": True}]
        }
        self.expected_result = {
            "aggregator": "ALL",
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
            },
        }
        return super().setUp()
    
    def test_jsonify_all_aggregator(self):
        result = self.aggregator.jsonify(object=self.object)

        self.assertEqual(result, self.expected_result)


class TestJsonifyAnyAggregator(unittest.TestCase):
    def setUp(self) -> None:
        self.aggregator = Aggregator(
            aggregator="ANY",
            field="dummy_aggregate_field",
            rule=BooleanOperation(
                inputs=[
                    Input(
                        field="dummy_boolean_operation_field", type="boolean"
                    ),
                    Input(type="boolean", value=True),
                ],
                operator=Operator.eval_equal,
            )
        )
        self.object = {
            "dummy_aggregate_field": [{"dummy_boolean_operation_field": True}]
        }
        self.expected_result = {
            "aggregator": "ANY",
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
            },
        }
        return super().setUp()
    
    def test_jsonify_any_aggregator(self):
        result = self.aggregator.jsonify(object=self.object)

        self.assertEqual(result, self.expected_result)


class TestEvaluateAllAggregator(unittest.TestCase):
    def setUp(self) -> None:
        self.aggregator = Aggregator(
            aggregator="ALL",
            field="dummy_aggregate_field",
            rule=BooleanOperation(
                inputs=[
                    Input(
                        field="dummy_boolean_operation_field",
                        type="boolean",
                    ),
                    Input(type="boolean", value=True),
                ],
                operator=Operator.eval_equal,
            )
        )
        self.object = {
            "dummy_aggregate_field": [
                {"dummy_boolean_operation_field": True},
                {"dummy_boolean_operation_field": False}
            ]
        }
        return super().setUp()
    
    def test_evaluate_all_aggregator(self):
        result = self.aggregator.evaluate(object=self.object)

        self.assertFalse(result)


class TestEvaluateAnyAggregator(unittest.TestCase):
    def setUp(self) -> None:
        self.aggregator = Aggregator(
            aggregator="ANY",
            field="dummy_aggregate_field",
            rule=BooleanOperation(
                inputs=[
                    Input(
                        field="dummy_boolean_operation_field",
                        type="boolean",
                    ),
                    Input(type="boolean", value=True),
                ],
                operator=Operator.eval_equal,
            )
        )
        self.object = {
            "dummy_aggregate_field": [
                {"dummy_boolean_operation_field": True},
                {"dummy_boolean_operation_field": False}
            ]
        }
        return super().setUp()
    
    def test_evaluate_any_aggregator(self):
        result = self.aggregator.evaluate(object=self.object)

        self.assertTrue(result)
