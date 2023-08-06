from abc import abstractmethod

from jqqb.helpers import get_object_item
from jqqb.rule import RuleInterface


class AggregatorInterface(RuleInterface):
    """Aggregator interface.
    
    Methods from this class must/could be (re)defined,
    until the signature is respected.
    """
    def __init__(self, field: str) -> None:
        self.field = field

    @abstractmethod
    def evaluate(self, object: dict) -> bool:
        ...

    @abstractmethod
    def jsonify(self, object: dict) -> dict:
        ...


class _AllAnyAggregator(AggregatorInterface):
    def __init__(
        self, field: str, rule: RuleInterface
    ) -> None:
        super().__init__(field=field)
        self.rule = rule

    @property
    @abstractmethod
    def _FUNCTION(cls):
        ...

    @property
    @abstractmethod
    def _FUNCTION_NAME(cls):
        ...

    def evaluate(self, object: dict) -> bool:
        aggregate = get_object_item(object=object, field=self.field)
        return False if aggregate is None else self._FUNCTION([
            self.rule.evaluate(object=aggregate_item)
            for aggregate_item in aggregate
        ])

    def jsonify(self, object: dict) -> dict:
        return {
            "aggregator": self._FUNCTION_NAME,
            "field": self.field,
            "rule": self.rule.jsonify(object=object),
        }


class AllAggregator(_AllAnyAggregator):
    _FUNCTION = all
    _FUNCTION_NAME = "ALL"


class AnyAggregator(_AllAnyAggregator):
    _FUNCTION = any
    _FUNCTION_NAME = "ANY"


class Aggregator:
    """Aggregator facade
    
    This facade provides constructors that return specific classes,
    then the other operations are directly managed by these classes
    following the same interface.
    """
    _AGGREGATORS = {"ALL": AllAggregator, "ANY": AnyAggregator}

    def __new__(
        cls, aggregator: str, field: str, **aggregator_kwargs
    ) -> "AggregatorInterface":
        return cls._AGGREGATORS[aggregator.upper()](
            field=field, **aggregator_kwargs
        )
