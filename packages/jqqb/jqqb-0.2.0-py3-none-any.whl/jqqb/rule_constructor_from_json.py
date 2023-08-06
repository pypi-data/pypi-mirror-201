import json
from typing import Union

from jqqb.aggregator import Aggregator, AggregatorInterface
from jqqb.boolean_operation import BooleanOperation
from jqqb.input import Input
from jqqb.operator import Operator
from jqqb.rule_connective import RuleConnective
from jqqb.rule import RuleInterface


class RuleConstructorFromJson:
    """Rule constructor usin a Json input.
    
    This class has been made to avoid circular dependency
    for RuleInterface subclasses that contain other RuleInterface instances.
    """
    def _load_json(self, json_entry: Union[str, dict]) -> dict:
        return (
            json.loads(json_entry)
            if isinstance(json_entry, str)
            else json_entry
        )

    def create_rule_from_json(
        self, json_entry: Union[str, dict]
    ) -> RuleInterface:
        parsed_json_entry = self._load_json(json_entry=json_entry)

        if "condition" in parsed_json_entry:
            rule = self.create_rule_connective_from_json(json_entry=json_entry)
        elif "operator" in parsed_json_entry:
            rule = self.create_boolean_operation_from_json(
                json_entry=json_entry
            )
        elif "aggregator" in parsed_json_entry:
            rule = self.create_aggregator_from_json(json_entry=json_entry)

        return rule

    def create_aggregator_from_json(
        self, json_entry: Union[str, dict]
    ) -> AggregatorInterface:
        parsed_json_entry = self._load_json(json_entry=json_entry)

        return Aggregator(
            aggregator=parsed_json_entry["aggregator"],
            field=parsed_json_entry["field"],
            rule=self.create_rule_from_json(
                json_entry=parsed_json_entry["rule"]
            )
        )

    def create_boolean_operation_from_json(
        self, json_entry: Union[str, dict]
    ) -> BooleanOperation:
        parsed_json_entry = self._load_json(json_entry=json_entry)

        return BooleanOperation(
            operator=Operator.get_operator(parsed_json_entry["operator"]),
            inputs=[
                Input(
                    **{
                        k: v
                        for k, v in parsed_json_entry_input.items()
                        if k in ("field", "type", "value")
                    }
                )
                for parsed_json_entry_input
                in parsed_json_entry["inputs"]
            ]
        )

    def create_rule_connective_from_json(
        self, json_entry: Union[str, dict]
    ) -> RuleConnective:
        parsed_json_entry = self._load_json(json_entry=json_entry)

        return RuleConnective(
            condition=parsed_json_entry["condition"],
            rules=[
                self.create_rule_from_json(
                    json_entry=parsed_json_entry_rule
                ) for parsed_json_entry_rule in parsed_json_entry["rules"]
            ]
        )
