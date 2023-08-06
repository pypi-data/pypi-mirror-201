from typing import Literal

from jqqb.rule import RuleInterface


class RuleConnective(RuleInterface):
    _CONDITIONS = {"AND": all, "OR": any}

    def __init__(
        self, condition: Literal["AND", "OR"], rules: list[RuleInterface]
    ):
        self.condition = condition
        self.condition_operation = self._CONDITIONS[condition]
        self.rules = rules

    def evaluate(self, object: dict) -> bool:
        return self.condition_operation(
            [rule.evaluate(object) for rule in self.rules]
        )

    def jsonify(self, object: dict) -> dict:
        return {
            "condition": self.condition,
            "rules": [rule.jsonify(object=object) for rule in self.rules],
        }
