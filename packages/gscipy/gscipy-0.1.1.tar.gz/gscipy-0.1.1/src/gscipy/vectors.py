"""Module."""
from __future__ import annotations

__author__ = "Matteo Gabba"
__copyright__ = "Copyright 2022, all right reserved Gabba Scientific"
__status__ = "Development"

from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import Any

import numpy as np

from gscipy.csv_io import CSVReader
from gscipy.decorators import check_args_len
from gscipy.general import TypeCheckedList
from gscipy.json_io import CustomJSONDict, JsonIOInterface


class VectorNDim:
    """Represents a vector in a multi-dimensional space.

    A vector instance is instantiated by key-word only arguments.

    >>> v = VectorNDim(x0=1, x1=1, x2=1, x3=1)

    Each coordinate is assigned to a class attribute
    >>> v.x0
    1.0
    >>> v.x1
    1.0
    >>> v.x2
    1.0
    >>> v.x3
    1.0

    The following operations are implemented by operator overloading:

    Get the total number of coordinates (vector length)
    >>> len(v)
    4

    Absolute value (magnitude)
    >>> v.magnitude
    2.0
    >>> abs(v)
    2.0

    Add vector inplace
    >>> v = VectorNDim(x0=1, x1=1, x2=1, x3=1)
    >>> v
    Vector(1.0, 1.0, 1.0, 1.0)
    >>> v += v
    >>> v
    Vector(2.0, 2.0, 2.0, 2.0)
    >>> v += v
    >>> v
    Vector(4.0, 4.0, 4.0, 4.0)

    Get coordinate by index
    >>> v = VectorNDim(x0=1, x1=1, x2=1, x3=1)
    >>> v[1]
    1.0

    Set coordinate by index
    >>> v[1] = 10
    >>> v
    Vector(1.0, 10, 1.0, 1.0)

    Iterate over the vector coordinates
    >>> [c for c in v]
    [1.0, 10, 1.0, 1.0]

    Dot product:
    >>> v1 = VectorNDim(x0=1, x1=1, x2=1, x3=1)
    >>> v2 = VectorNDim(x0=2, x1=2, x2=2, x3=2)

    >>> v1.dot(v2)
    8.0
    >>> v1 @ v2
    8.0

    Vector addition
    >>> v1 + v2
    Vector(3.0, 3.0, 3.0, 3.0)

    Vector substraction
    >>> v1 - v2
    Vector(-1.0, -1.0, -1.0, -1.0)

    Coordinate-wise and scalar multiplication
    >>> v1 * v2
    Vector(2.0, 2.0, 2.0, 2.0)

    Multiplication by a constant
    >>> v1 * 5
    Vector(5.0, 5.0, 5.0, 5.0)

    Inversion
    >>> -v1
    Vector(-1.0, -1.0, -1.0, -1.0)

    Raising to the power of a number (int or float)
    >>> v2 ** 2
    Vector(4.0, 4.0, 4.0, 4.0)

    Vector comparison
    >>> v1 = VectorNDim(x0=1, x1=1, x2=1, x3=1)
    >>> v2 = VectorNDim(x0=2, x1=2, x2=2, x3=2)
    >>> v1 == v1
    True
    >>> v1 == v2
    False
    >>> v1 != v2
    True

    See: See: https://gist.github.com/gmalmquist/6b0ee1c38d7263f6158f
    """

    def __init__(self, **coordinates: float | int | str) -> None:

        self._class_name = self.__class__.__name__

        # Set keyword arguments to attributes
        for key, value in coordinates.items():
            try:
                setattr(self, key, float(value))
            except ValueError as error:
                raise TypeError(
                    f"{self._class_name}() argument must be a list of float(s) or int(s),"
                    f" or float-convertible string numbers, not '{value.__class__.__name__}'"
                ) from error

        # Set coordinates attribute
        self._coordinates = list(map(float, coordinates.values()))
        self._keys = list(coordinates.keys())

    @property
    def magnitude(self) -> float:
        """Vector magnitude (absolute value).

        >>> v = VectorNDim(x0=1, x1=1)
        >>> v.magnitude
        1.4142135623730951
        """
        return sum(self**2) ** 0.5

    @check_args_len
    def dot(self, other: VectorNDim) -> float:
        """Dot product (inner product) between vectors of same dimension.

        >>> v = VectorNDim(x0=1, x1=1)
        >>> v.dot(v)
        2.0

        raise TypeError if 'other' is not a vector.
        """
        if isinstance(other, self.__class__):
            return sum(self * other)
        raise TypeError(
            f"unsupported operand type(s) for {self._class_name}.dot():"
            f" '{other.__class__.__name__}'"
        )

    def __call__(self, **coordinates: float) -> VectorNDim:
        """Make Vector instances callable.

        >>> v = VectorNDim()
        >>> v
        Vector()
        >>> v1 = v(x1=1, x2=1)
        >>> v1
        Vector(1.0, 1.0)
        """
        return self.__class__(**coordinates)

    def __getitem__(self, index: int) -> float:
        """Get vector coordinate by index or slicing.

        >>> v = VectorNDim(x0=1, x1=2)
        >>> v[0]
        1.0
        """
        return self._coordinates[index]

    def __setitem__(self, index: int, value: int | float) -> None:
        """Set vector coordinate by index.

        >>> v = VectorNDim(x0=1, x1=2)
        >>> v
        Vector(1.0, 2.0)
        >>> v[1] = 123
        >>> v
        Vector(1.0, 123)

        Raise TypeError if 'value' is not a float or int number.
        """
        if isinstance(value, (int, float)):
            self._coordinates[index] = value
            # Update value of all attributes derived from self._coordinates
            unprotected_keys = [
                key for key in self.__dict__.keys() if not key.startswith("_")
            ]
            for i, key in enumerate(unprotected_keys):
                setattr(self, key, self._coordinates[i])
        else:
            raise TypeError(
                f"unsupported operand type(s) for {self._class_name}.__setitem__():"
                f" '{value.__class__.__name__}'"
            )

    def __iter__(self) -> Iterator[float]:
        """Allows iteration over the vector coordinates.

        >>> v = VectorNDim(x1=1, x2=2)
        >>> [c for c in v]
        [1.0, 2.0]
        """
        return iter(self._coordinates)

    def __len__(self) -> int:
        """Returns vector length (number of coordinates).

        >>> v = VectorNDim(x1=1, x2=2)
        >>> len(v)
        2
        """
        return len(self._coordinates)

    @check_args_len
    def __add__(self, other: VectorNDim) -> VectorNDim:
        """Vector addition.

        >>> v1 = VectorNDim(x0=1, x1=1)
        >>> v2 = VectorNDim(x0=2, x1=2)
        >>> v1 + v2
        Vector(3.0, 3.0)

        Raise AssertionError if the two vectors have different dimension.
        Raise TypeError if 'other' is not a vector.
        """
        if isinstance(other, self.__class__):
            return self(
                **{
                    self._keys[i]: c1 + c2
                    for i, (c1, c2) in enumerate(zip(self, other))
                }
            )
        return NotImplemented

    def __radd__(self, other: VectorNDim) -> VectorNDim:
        return self + other

    @check_args_len
    def __iadd__(self, other: VectorNDim) -> VectorNDim:
        """Inplace vector addition.

        >>> v = VectorNDim(x1=1, x2=1)
        >>> v += v
        >>> v
        Vector(2.0, 2.0)

        Raise AssertionError if the two vectors have different dimension.
        Raise TypeError if 'other' is not a vector.
        """
        if isinstance(other, self.__class__):
            return self(
                **{
                    self._keys[i]: c1 + c2
                    for i, (c1, c2) in enumerate(zip(self, other))
                }
            )
        return NotImplemented

    @check_args_len
    def __sub__(self, other: VectorNDim) -> VectorNDim:
        """Vector subtraction.

        >>> v1 = VectorNDim(x0=1, x1=1)
        >>> v2 = VectorNDim(x0=2, x1=2)
        >>> v1 - v2
        Vector(-1.0, -1.0)

        Raise AssertionError if the two vectors have different dimension.
        Raise TypeError if 'other' is not a vector.
        """
        if isinstance(other, self.__class__):
            return self + (-other)
        return NotImplemented

    def __rsub__(self, other: VectorNDim) -> VectorNDim:
        return other + (-self)

    @check_args_len
    def __mul__(self, other: VectorNDim | int | float) -> VectorNDim:
        """Coordinate-wise vector multiplication and scalar multiplication of a vector.

        >>> v1 = VectorNDim(x0=1, x1=1)
        >>> v2 = VectorNDim(x0=2, x1=2)
        >>> v1 * v2
        Vector(2.0, 2.0)
        >>> v1 * 10
        Vector(10.0, 10.0)

        Raise AssertionError if the two vectors have different dimension.
        Raise TypeError if 'other' is not a Vector instance or a number (int, float).
        """
        if isinstance(other, self.__class__):
            return self(
                **{
                    self._keys[i]: a * b
                    for i, (a, b) in enumerate(zip(self, other))
                }
            )
        if isinstance(other, (int, float)):
            return self(
                **{self._keys[i]: a * other for i, a in enumerate(self)}
            )
        return NotImplemented

    def __rmul__(self, other: VectorNDim | int | float) -> VectorNDim:
        return self * other

    def __matmul__(self, other: VectorNDim) -> float:
        """Overload @ operator with dot product."""
        return self.dot(other)

    def __pow__(self, power: int | float) -> VectorNDim:
        """Vector raise to the power.

        >>> v = VectorNDim(x0=4, x1=4)
        >>> v ** 2
        Vector(16.0, 16.0)
        >>> v ** 0.5
        Vector(2.0, 2.0)

        Raise TypeError if 'power' is not a number of type int or float.
        """
        if isinstance(power, (int, float)):
            return self(
                **{self._keys[i]: c**power for i, c in enumerate(self)}
            )
        return NotImplemented

    def __neg__(self) -> VectorNDim:
        """Inverse vector.

        >>> v = VectorNDim(x1=1, x2=1)
        >>> -v
        Vector(-1.0, -1.0)
        """
        return self(**{self._keys[i]: -c for i, c in enumerate(self)})

    def __pos__(self) -> VectorNDim:
        return self

    def __abs__(self) -> float:
        """Absolute value (vector magnitude).

        >>> v = VectorNDim(x0=1, x1=1)
        >>> abs(v)
        1.4142135623730951
        """
        return self.magnitude

    @check_args_len
    def __eq__(self, other: VectorNDim | int | float) -> bool:
        """Check vector equality in terms of both magnitude and direction.

        >>> v1 = VectorNDim(x0=1, x1=2)
        >>> v2 = VectorNDim(x0=2, x1=3)
        >>> v1 == v2
        False
        >>> v1 == v1
        True

        Raise AssertionError if the two vectors have different dimensions.
        """
        if isinstance(other, self.__class__):
            return all(
                a == b for a, b in zip(self._coordinates, other._coordinates)
            )
        return NotImplemented

    def __ne__(self, other: VectorNDim | int | float) -> bool:
        """Check vector vector inequality in terms of both magnitude and direction.

        >>> v1 = VectorNDim(x0=1, x1=2)
        >>> v2 = VectorNDim(x0=2, x1=3)
        >>> v1 != v2
        True
        >>> v1 != v1
        False
        """
        return not self == other

    def __hash__(self) -> int:
        """Return hash value of the given instance."""
        return hash(tuple(self))

    def __bool__(self) -> bool:
        """Check that all coordinates are null."""
        return all(v == 0 for v in self)

    def __repr__(self) -> str:
        """Returns a representation of a Vector object.

        >>> v = VectorNDim(x1=1, x2=3)
        >>> v
        Vector(1.0, 3.0)
        """
        return f"{self._class_name}({', '.join(str(c) for c in self._coordinates)})"

    def __str__(self) -> str:
        """Returns a string representation of a Vector object.

        >>> v = VectorNDim(x1=1, x2=3)
        >>> print(v)
        Vector(1.0, 3.0)
        """
        return f"{self._class_name}({', '.join(str(c) for c in self._coordinates)})"


class Vector(VectorNDim, JsonIOInterface):
    """Represents a vector in 3-dimensions with coordinates (x, y, z).

    >>> r = Vector(x=1, y=2, z=3)
    >>> r
    Position(1, 2, 3)

    Coordinates are set to zero by default
    >>> r = Vector(x=1, y=2)
    >>> r
    Position(1, 2, 0)

    Implement cross-product
    >>> r1 = Vector(x=1, y=2, z=2)
    >>> r2 = Vector(x1=2, y=3)
    >>> r1 ^ r2
    Position(-6.0, 4.0, -1.0)
    >>> r1.cross(r1)
    Position(-6.0, 4.0, -1.0)
    """

    def __init__(self, *, x: float = 0, y: float = 0, z: float = 0) -> None:
        """
        X : float, optional, default to 0.

        y : float, optional, default to 0
        z : float, optional, default to 0
        """
        super().__init__(x=x, y=y, z=z)

    # __slots__ = ["x", "y", "z"]

    @classmethod
    def from_json(cls, json_dict: CustomJSONDict) -> Vector:
        return cls(x=json_dict["x"], y=json_dict["y"], z=json_dict["z"])

    def to_json(self) -> CustomJSONDict:
        obj_dict = {"x": self.x, "y": self.y, "z": self.z}
        json_dict = CustomJSONDict(obj_dict)
        json_dict["__class__"] = self._get__class__()
        return json_dict

    def cross(self, other: Vector) -> Vector:
        """VectorNDim cross product.

        >>> r1 = Vector(x=1, y=2, z=2)
        >>> r2 = Vector(x1=2, y=3)
        >>> r1.cross(r1)
        Position(-6.0, 4.0, -1.0)

        Raise TypeError if 'other' is not a vector.
        """
        if isinstance(other, self.__class__):
            return self ^ other
        raise TypeError(
            f"unsupported operand type(s) for {self._class_name}.cross():"
            f" '{other.__class__.__name__}'"
        )

    def __xor__(self, other: Vector) -> Vector:
        """VectorNDim cross product.

        >>> r1 = Vector(x=1, y=2, z=2)
        >>> r2 = Vector(x1=2, y=3)
        >>> r1 ^ r2
        Position(-6.0, 4.0, -1.0)
        """
        if isinstance(other, self.__class__):
            return self(
                **{
                    self._keys[i]: c
                    for i, c in enumerate(np.cross(self, other))
                }
            )
        return NotImplemented


class VectorsList(TypeCheckedList):
    """Type checked list of 3D vectors.

    >>> vectors = VectorsList([])
    >>> vectors
    VectorsList([])

    Implement a load() method for loading vectors from an iterator (for example from a .csv file row iterator).
    Raise TypeError if a not Vector instance is appended or inserted (in)to the list.
    """

    def __init__(self, iterator_arg: list[Vector] = None):
        """
        Iterator_arg : List[Vector], optional, default to None.

            List of Vector vectors
        """
        # Initialize the parent class to type check for Vector instances
        super().__init__(iterator_arg=iterator_arg, instance_type=Vector)

    @classmethod
    def from_json(cls, json_dict: CustomJSONDict) -> VectorsList:

        return cls(json_dict["data"])

    def load(self, row_iter: Iterable[dict[str, Any]]) -> None:
        """Load 3D vectors into the type checked list.

        Parameters
        ----------
        row_iter : Iterable[dict[str, Any]]
            Iterable generating a dictionary dict[str, Any] with keys {'x', 'y', 'z'}.
            For example, the row-iterator of a .csv file.

        Returns
        -------
            A type checked list populated with Vector vectors
        """
        for row in row_iter:

            self.append(Vector(**row))


class VectorListLoader:
    """Loads 3D vectors into a type-checked list given the column names corresponding to the 3D coordinates values.

    (x, y, z), or a subset of those, as stored in the input file.

    >>> source = Path.cwd() / "data" / "sub1.csv"
    >>> usecols = ['gaze_deg_coord_x', 'gaze_deg_coord_y']
    >>> vectors_loader = VectorListLoader(source, usecols)
    >>> vectors = vectors_loader.load()
    >>> vectors[:3]
    VectorsList([Vector(0.4622481497169438, 3.76608427632374, 0.0),
             Vector(0.46393828577858687, 3.7411490072433953, 0.0),
             Vector(0.456283375837779, 3.7295640810489856, 0.0)])

    The coordinates, as given by the column names, are automatically re-named to pre-defined names: 'x', 'y', 'z'

    >>> vectors[0].__dict__
    {'_class_name': 'Vector',
     'x': 0.4622481497169438,
     'y': 3.76608427632374,
     'z': 0.0,
     '_coordinates': [0.4622481497169438, 3.76608427632374, 0.0],
     '_keys': ['x', 'y', 'z']}
    """

    # Pre-defined 3D coordinates names
    new_names = ["x", "y", "z"]

    def __init__(self, source: Path, usecols: list[str]) -> None:
        """
        ---

            source : Path, required
                Path of the input file.

            usecols : List or Tuple, required
                Names corresponding to the coordinates (x, y, z) of a 3D vector, or a subset of those,
                as stored in the input file.
        """
        self.source = source
        self.usecols = usecols

        # Map given coordinates names to pre-defined names
        self.col_map_dict = dict(zip(self.usecols, self.new_names))

    def load(self) -> VectorsList:
        """Loads 3D vectors into the type checked list from .csv file.

        Returns
        -------
            A type checked list populated with 3D vectors.
        """
        vectors = VectorsList()
        csv_reader = CSVReader(self.source)
        row_iter = csv_reader.row_iter(
            usecols=self.usecols, col_map_dict=self.col_map_dict
        )
        vectors.load(row_iter)

        return vectors
