from typing import Union

from jqqb.rule import RuleInterface
from jqqb.rule_constructor_from_json import RuleConstructorFromJson


class QueryBuilder:
    RULE_CONSTRUCTOR_FROM_JSON = RuleConstructorFromJson()

    def __init__(self, rule: RuleInterface):
        self.rule = rule

    @classmethod
    def create_from_json(
        cls, json_entry: Union[str, dict]
    ) -> "QueryBuilder":
        """Construct a QueryBuilder instance from a given JSON."""
        return cls(
            rule=cls.RULE_CONSTRUCTOR_FROM_JSON.create_rule_from_json(
                json_entry=json_entry
            )
        )

    def match_objects(self, objects: list[dict]) -> list[dict]:
        return [
            object for object in objects if self.object_matches_rules(object)
        ]

    def object_matches_rules(self, object: dict) -> dict:
        return self.rule.evaluate(object)
