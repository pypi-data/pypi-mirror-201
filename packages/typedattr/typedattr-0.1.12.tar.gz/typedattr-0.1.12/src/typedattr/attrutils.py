from typing import List

from attr import fields

from typedattr.typeutils import AttrsClass


def get_attr_names(cls: AttrsClass) -> List[str]:
    """Get all attribute names of an attrs class."""
    return [att.name for att in fields(cls)]  # noqa
