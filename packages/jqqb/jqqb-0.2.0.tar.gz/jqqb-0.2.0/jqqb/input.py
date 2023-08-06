from datetime import date, datetime, time
from typing import Any, Optional

from jqqb.helpers import get_object_item


class Input:
    class NotRetrievedValue:
        pass

    _CAST_FUNCTIONS = {
        "boolean": bool,
        "datetime": lambda x: (
            datetime.fromisoformat(x) if isinstance(x, str) else x
        ),
        "date": lambda x: date.fromisoformat(x) if isinstance(x, str) else x,
        "double": float,
        "integer": int,
        "string": str,
        "time": lambda x: time.fromisoformat(x) if isinstance(x, str) else x,
    }

    def __init__(
        self,
        type: str,
        field: Optional[str] = None,
        value: Any = NotRetrievedValue,
    ) -> None:
        self.field = field
        self.type = type
        self.value = value

    def get_value(self, object: Optional[dict] = None) -> Any:
        return self.typecast_value(
            value_to_cast=get_object_item(object=object, field=self.field)
            if self.field else self.value
        )

    def jsonify(self, object: dict) -> dict:
        json_result = {"type": self.type}

        if self.field:
            json_result["field"] = self.field

        if self.value is not self.NotRetrievedValue:
            json_result["value"] = self.value

        return json_result

    def typecast_value(self, value_to_cast: Any) -> Any:
        cast_function = self._CAST_FUNCTIONS.get(self.type)

        if (
            value_to_cast in (None, self.NotRetrievedValue)
            or cast_function is None
        ):
            return value_to_cast

        return cast_function(value_to_cast)
