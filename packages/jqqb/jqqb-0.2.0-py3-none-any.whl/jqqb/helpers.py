from functools import reduce


def get_object_item(object: dict, field: str):
    fields = field.split(".")
    return reduce(
        lambda x, y:
            x if y == ""
            else x.get(y) if isinstance(x, dict)
            else x[int(y)] if isinstance(x, list) and len(x) > 0
            else None,
        fields,
        object,
    )
