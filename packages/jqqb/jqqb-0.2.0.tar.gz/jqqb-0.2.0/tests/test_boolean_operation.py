import unittest

from jqqb.input import Input
from jqqb.operator import Operator
from jqqb.boolean_operation import BooleanOperation


class TestBooleanOperationJsonify(unittest.TestCase):
    def setUp(self) -> None:
        self.object = {"dummy_key": "dummy_value"}
        self.expected_result = {
            "operator": "equal",
            "inputs": [
                {"field": "dummy_key", "type": "str"},
                {"value": "dummy_value", "type": "str"},
            ],
        }
        return super().setUp()

    def test_boolean_operation_jsonify(self):
        boolean_operation = BooleanOperation(
            operator=Operator.eval_equal,
            inputs=[
                Input(type="str", field="dummy_key"),
                Input(type="str", value="dummy_value"),
            ],
        )
        result = boolean_operation.jsonify(object=self.object)

        self.assertEqual(result, self.expected_result)


class TestBooleanOperationEvaluate(unittest.TestCase):
    def setUp(self) -> None:
        self.object = {
            "dummy_key1": "dummy_value",
            "dummy_key2": "other_dummy_value",
            "dummy_key3": "dummy_value",
        }
        return super().setUp()

    def test_boolean_operation_evaluate_field_and_value_true(self):
        boolean_operation = BooleanOperation(
            operator=Operator.eval_equal,
            inputs=[
                Input(type="str", field="dummy_key1"),
                Input(type="str", value="dummy_value"),
            ],
        )
        result = boolean_operation.evaluate(object=self.object)

        self.assertTrue(result)

    def test_boolean_operation_evaluate_field_and_value_false(self):
        boolean_operation = BooleanOperation(
            operator=Operator.eval_equal,
            inputs=[
                Input(type="str", field="dummy_key1"),
                Input(type="str", value="other_dummy_value"),
            ],
        )
        result = boolean_operation.evaluate(object=self.object)

        self.assertFalse(result)

    def test_boolean_operation_evaluate_field_and_variable_true(self):
        boolean_operation = BooleanOperation(
            operator=Operator.eval_equal,
            inputs=[
                Input(type="str", field="dummy_key1"),
                Input(type="str", field="dummy_key3"),
            ],
        )
        result = boolean_operation.evaluate(object=self.object)

        self.assertTrue(result)

    def test_boolean_operation_evaluate_field_and_variable_false(self):
        boolean_operation = BooleanOperation(
            operator=Operator.eval_equal,
            inputs=[
                Input(type="str", field="dummy_key1"),
                Input(type="str", field="dummy_key2"),
            ],
        )
        result = boolean_operation.evaluate(object=self.object)

        self.assertFalse(result)
