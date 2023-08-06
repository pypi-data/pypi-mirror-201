from __future__ import annotations

from collections import UserList
from collections.abc import Iterable
from typing import Any

from gscipy.json_io import CustomJSONDict, JsonIOInterface

# TODO: add docstrings and type annotations


class TypeCheckedList(UserList, JsonIOInterface):
    """
    Type checked list of instances of the same class.

    See: https://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list
    """

    def __init__(
        self, iterator_arg: Iterable[Any] = None, instance_type: Any = float
    ) -> None:

        super().__init__()
        self._instance_type = instance_type
        if iterator_arg is not None:
            self.extend(iterator_arg)  # This validates the arguments...

    def to_json(self, obj_dict=None) -> CustomJSONDict:
        json_dict = CustomJSONDict({"data": list(self)})
        json_dict["__class__"] = self._get__class__()
        return json_dict

    def _check_type(self, instance):
        if not isinstance(instance, self._instance_type):
            raise TypeError(
                f"{self.__class__.__name__} is a collection of {self._instance_type} instances"
                f" but {instance} ({instance.__class__}) was passed instead"
            )

        return instance

    def insert(self, i, item):
        return super().insert(i, self._check_type(item))

    def append(self, item):
        return super().append(self._check_type(item))

    def extend(self, other):
        return super().extend([self._check_type(v) for v in other])

    def __call__(self, iterator_arg: Iterable[Any]) -> TypeCheckedList:
        return self.__class__(iterator_arg)

    def __setitem__(self, i, other):
        if isinstance(i, slice):
            return super().__setitem__(
                i, [self._check_type(v) for v in other]
            )  # Extended slice...
        return super().__setitem__(i, self._check_type(other))

    def __add__(self, other):
        return super().__add__([self._check_type(v) for v in other])

    def __iadd__(self, other):
        return super().__iadd__([self._check_type(v) for v in other])

    def __repr__(self):
        return f"{self.__class__.__name__}({[item for item in self]})"
