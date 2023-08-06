"""Module for handling data input/output from and to files."""
from __future__ import annotations

__author__ = "Matteo Gabba"
__copyright__ = "Copyright 2022, all right reserved Gabba Scientific"
__status__ = "Development"

import json
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from pathlib import Path
from pydoc import locate
from typing import Any

import numpy as np

JSONType = str, dict | int | float | str | list | bool | None


class CustomJSONDict(dict):
    """Dictionary satisfying JSON decodable / encodable interface."""

    def __init__(
        self,
        data: Mapping[str, JSONType] | Iterable[str, JSONType] = None,
        **kwargs: JSONType,
    ) -> None:
        if not data:
            super().__init__()
        if data:
            super().__init__(data)
        if kwargs:
            super().__init__(**kwargs)
        self["__class__"] = None


class JsonIOInterfaceError(BaseException):
    pass


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> CustomJSONDict | JSONType:

        if isinstance(obj, np.integer):
            return int(obj)

        if isinstance(obj, type):
            return str(obj.__name__)

        if isinstance(obj, Path):
            json_dict = CustomJSONDict(path=str(obj))
            json_dict["__class__"] = "pathlib.Path"
            return json_dict

        if isinstance(obj, np.ndarray):
            json_dict = CustomJSONDict(array=obj.tolist())
            json_dict["__class__"] = "numpy.ndarray"
            return json_dict

        else:
            try:
                return obj.to_json()
            except AttributeError as error:
                raise JsonIOInterfaceError(
                    f"missing method to_json() in class: '{obj.__class__.__name__}'"
                ) from error
            except TypeError:
                pass

        # Let the base class default method raise the TypeError
        return super().default(obj)


class CustomObjectJSONDumper:
    """Dump custom objects to JSON file."""

    def __init__(self, output_path: Path, obj: Any) -> None:
        self.output_path = output_path
        self.obj = obj

    def dump(self) -> None:
        with open(self.output_path, "w", encoding="utf-8") as file:
            json_data = json.dumps(self.obj, cls=CustomJSONEncoder, indent=4)
            file.write(json_data)


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        kwargs["object_hook"] = self.object_hook
        super().__init__(**kwargs)

    def object_hook(self, json_dict: CustomJSONDict) -> Any:

        try:
            __class__ = json_dict.pop("__class__")
        except KeyError as error:
            raise JsonIOInterfaceError(
                f"missing field name '__class__' in JSON object: {json_dict}"
            ) from error

        try:
            cls = locate(__class__)
        except KeyError as error:
            raise JsonIOInterfaceError(
                f"JSON object '{__class__}' not found"
            ) from error

        # Handle patlib.Path
        if cls is Path:
            obj = Path(json_dict["path"])
            return obj

        # Handle numpy.ndarray
        if cls is np.ndarray:
            obj = np.array(json_dict["array"])
            return obj

        if hasattr(cls, "from_json"):
            obj = cls().from_json(json_dict)
            return obj

        else:
            raise JsonIOInterfaceError(
                f"missing method from_json() in class: '{cls.__class__.__name__}'"
            )


class JSONLoader:
    """Load JSON object using CustomJSONEncoder."""

    def __init__(self, input_path: Path) -> None:
        self.input_path = input_path

    @staticmethod
    def _parse_invalid_json_values(value: str) -> float:
        conversion = {
            "-Infinity": -float("inf"),
            "Infinity": float("inf"),
            "NaN": float("nan"),
        }
        return conversion[value]

    def load(self) -> Any:
        with open(self.input_path, "r", encoding="utf-8") as file:
            json_data = file.read()
            obj = json.loads(
                json_data,
                cls=CustomJSONDecoder,
                parse_constant=self._parse_invalid_json_values,
            )

        return obj


class BaseJsonIOInterface(ABC):
    """Interface of JSON encodable / decodable objects."""

    @classmethod
    @abstractmethod
    def from_json(cls, json_dict: CustomJSONDict) -> Any:
        ...

    @abstractmethod
    def to_json(self) -> CustomJSONDict:
        ...


class DefaultJsonIOMixin:
    @classmethod
    def from_json(cls, json_dict: CustomJSONDict) -> Any:

        obj = cls()

        for key, value in json_dict.items():

            try:
                getattr(obj, key)
            except AttributeError as error:
                raise AttributeError(
                    f"invalid attribute '{key}' for class: '{cls.__class__.__name__}'"
                ) from error

            try:
                __class__ = value.pop("__class__")
            except (KeyError, AttributeError, TypeError):
                obj.__dict__[key] = value
                continue

            try:
                _cls = locate(__class__)
            except KeyError as error:
                raise JsonIOInterfaceError(
                    f"class '{__class__}' not found'"
                ) from error

            # Handle patlib.Path
            if _cls is Path:
                obj.__dict__[key] = Path(value)
                continue

            # Handle numpy.ndarray
            if _cls is np.ndarray:
                obj.__dict__[key] = np.array(value)
                continue

            # Handle custom objects
            if hasattr(_cls, "from_json"):
                try:
                    obj.__dict__[key] = json.loads(
                        value, cls=CustomJSONDecoder
                    )
                except TypeError:
                    pass

            elif not hasattr(_cls, "from_json"):
                raise JsonIOInterfaceError(
                    f"missing method from_json() in class: '{obj.__class__.__name__}'"
                )

        # Let the base class default method raise the TypeError
        return obj

    def _get__class__(self) -> str:
        return ".".join([self.__module__, self.__class__.__name__])

    def to_json(self) -> CustomJSONDict:
        json_dict = CustomJSONDict(self.__dict__)
        json_dict["__class__"] = self._get__class__()
        return json_dict


class JsonIOInterface(DefaultJsonIOMixin, BaseJsonIOInterface):
    pass
