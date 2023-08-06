from jqqb.input import Input
from jqqb.operator import Operator
from jqqb.rule import RuleInterface


class BooleanOperation(RuleInterface):
    def __init__(self, operator: Operator, inputs: list[Input]):
        self.inputs = inputs
        self.operator = operator

    def evaluate(self, object: dict) -> bool:
        return self.operator(
            *[input.get_value(object=object) for input in self.inputs]
        )

    def jsonify(self, object: dict) -> dict:
        return {
            "inputs": [input.jsonify(object=object) for input in self.inputs],
            "operator": Operator.jsonify(operator=self.operator),
        }
