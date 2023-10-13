"""_summary_."""
import inspect
from dataclasses import fields, is_dataclass
from typing import Any


# NOTE: There is no type annotation for dataclasses
def get_dataclass_field_names(obj: Any) -> list[str]:
    """Returns the fields of a dataclass as a list of strings."""
    if not inspect.isclass(obj):
        raise ValueError(
            f"Argument data_cls should be a class, got {type(obj)}"
        )

    if not is_dataclass(obj):
        raise ValueError(f"'{obj.__name__}' is not a dataclass")

    return [field.name for field in fields(obj)]
