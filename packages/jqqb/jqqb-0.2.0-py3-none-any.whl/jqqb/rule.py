from abc import ABC, abstractmethod


class RuleInterface(ABC):
    @abstractmethod
    def evaluate(self, object: dict) -> bool:
        ...

    @abstractmethod
    def jsonify(self, object: dict) -> bool:
        ...
