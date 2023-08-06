"""Module."""

from __future__ import annotations

__author__ = "Matteo Gabba"
__copyright__ = "Copyright 2022, all right reserved Gabba Scientific"
__status__ = "Development"

import datetime
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from typing import Any

from pandas import to_datetime

from gscipy.csv_io import CSVReader
from gscipy.general import TypeCheckedList
from gscipy.json_io import CustomJSONDict, JsonIOInterface


class Time(JsonIOInterface):
    """Represents a time.

    A Time instance can be initialized by parsing:

    1) a datetime instance
    >>> from datetime import datetime
    >>> t = datetime.now()
    >>> t
    datetime.datetime(2022, 11, 24, 15, 56, 31, 591748)
    >>> Time(t)
    Time(1669301791.591748)

    2) a timestamp (float or int)
    >>> Time(t.timestamp())
    Time(1669301791.591748)
    >>> Time(123)
    Time(123)

    3) a timestamp-convertible string with the correct format
    >>> Time('2022-11-24 15:56:31.591748')
    Time(1669305391.591748)

    raise a TypeError otherwise.

    A Time instance can be modified using a property setter
    >>> t = Time(1)
    >>> t
    Time(1)
    >>> t.time = 2
    >>> t
    Time(2)

    Magic methods for addition, subtraction, multiplication, division, rising to the power, abs()
    and comparison (<, <=, ==, !=, >=, >) of Time instances or a Time instance with a constant (int, float)
    are implemented.
    """

    # __slots__ = ["time", "_time_str"]

    # Default string format for string parsing to a timestamp
    _time_str = "%Y-%m-%d %H:%M:%S.%f%Z"

    def __init__(self, value: datetime | float | int | str = 0) -> None:
        """
        ---

            value : (datetime, float, int, str), optional, default to 0
        """
        if not isinstance(value, (datetime, float, int, str)):
            raise TypeError(
                f"{self.__class__.__name__}() argument must be a timestamp ('float' or 'int'), a datetime"
                f" that can be converted to one, or a string of the format {self.__class__._time_str}"
                f" that can be parsed into one, not '{value.__class__.__name__}'"
            )
        self._time = value
        self.time = self._time

    @classmethod
    def from_json(cls, json_dict: CustomJSONDict) -> Time:
        return cls(json_dict["time"])

    def to_json(self) -> CustomJSONDict:
        json_dict = CustomJSONDict({"time": self.time})
        json_dict["__class__"] = self._get__class__()
        return json_dict

    @property
    def time(self) -> int | float:
        """Get time property.

        >>> t = Time(1)
        >>> t.time
        1
        """
        return self._time

    @time.setter
    def time(self, value: float | int | str | datetime) -> None:
        """Set time property from a datetime instance, a timestamp (float, int) or a timestamp-convertible string.

        >>> t = Time(1)
        >>> t.time = 2
        >>> t.time
        2
        >>> t
        Time(2)

        Parameters
        ----------
         value : (float, int, str, datetime), required
        """
        if not isinstance(value, (datetime, float, int, str)):
            raise TypeError(
                f"{self.__class__.__name__}() argument must be a timestamp ('float' or 'int'), a datetime"
                f" that can be converted to one, or a string of the format {self.__class__._time_str}"
                f" that can be parsed into one, not '{value.__class__.__name__}'"
            )

        if isinstance(value, datetime):
            try:
                value = value.timestamp()
            except Exception as error:
                raise ValueError(
                    f"{self.__class__.__name__}() could not create a valid timestamp from 'value'"
                ) from error

        elif isinstance(value, str):
            try:
                value = to_datetime(value).timestamp()
            except Exception as error:
                raise ValueError(
                    f"{self.__class__.__name__}() could not parse a valid timestamp "
                    f"from 'value' \n (provide a string with format: {self._time_str})"
                ) from error

        self._time = value

    def __call__(self, value: datetime | float | int | str):
        """Make Time instance callable.

        >>> t = Time()
        >>> t
        Time(0)
        >>> t1 = t(2)
        >>> t1
        Time(2)
        """
        return self.__class__(value)

    def __add__(self, other: Time | int | float) -> Time:
        """Add Times or constant to Time, raise TypeError otherwise.

        >>> t1 = Time(1)
        >>> t2 = Time(3)
        >>> t1 + t2
        Time(4)
        >>> t1 + 4
        Time(5)
        """
        if isinstance(other, Time):
            return Time(self.time + other.time)
        if isinstance(other, (int, float)):
            return Time(self.time + other)
        return NotImplemented

    def __radd__(self, other: Time | int | float) -> Time:
        return self + other

    def __sub__(self, other: Time | int | float) -> Time:
        """Subtracts Times or constant to Time, raise TypeError otherwise.

        >>> t1 = Time(1)
        >>> t2 = Time(3)
        >>> t1 - t2
        Time(-2)
        >>> t1 - 4
        Time(-3)
        """
        if isinstance(other, (Time, int, float)):
            return self + (-other)
        return NotImplemented

    def __rsub__(self, other: Time | int | float) -> Time:
        return other + (-self)

    def __mul__(self, other: Time | int | float) -> Time:
        """Multiply Times or constant to Time, raise TypeError otherwise.

        >>> t1 = Time(1)
        >>> t2 = Time(3)
        >>> t1 * t2
        Time(3)
        >>> t1 * 4
        Time(4)
        """
        if isinstance(other, Time):
            return Time(self.time * other.time)
        if isinstance(other, (int, float)):
            return Time(self.time * other)
        return NotImplemented

    def __rmul__(self, other: Time | int | float) -> Time:
        return self * other

    def __truediv__(self, other) -> Time:
        """Divide Times or constant to Time, raise TypeError otherwise.

        >>> t1 = Time(1)
        >>> t2 = Time(2)
        >>> t1 / t2
        Time(0.5)
        >>> t1 / 3
        Time(0.3333333333333333)
        """
        return self * (other**-1)

    def __rtruediv__(self, other) -> Time:
        return other / self

    def __pow__(self, power: int | float) -> Time:
        """Rise Time to the power, raise TypeError otherwise.

        >>> t = Time(4)
        >>> t ** 2
        Time(16)
        >>> t ** 0.5
        Time(2.0)
        """
        if isinstance(power, (int, float)):
            return Time(self.time**power)
        return NotImplemented

    def __neg__(self) -> Time:
        return Time(-self.time)

    def __abs__(self) -> Time:
        """Time absolute value.

        >>> t = Time(-1)
        >>> abs(t)
        Time(1)
        """
        return Time(abs(self.time))

    def __lt__(self, other: Time | int | float) -> bool:
        """Compares Time instances.

        >>> t1 = Time(1)
        >>> t2 = Time(2)
        >>> t1 < t2
        True
        >>> t1 < 0
        False
        """
        if isinstance(other, Time):
            return self.time < other.time
        if isinstance(other, (int, float)):
            return self.time < other
        return NotImplemented

    def __le__(self, other: Time | int | float) -> bool:
        """Compares Time instances.

        >>> t1 = Time(1)
        >>> t2 = Time(2)
        >>> t1 <= t2
        True
        >>> t1 <= 1
        True
        """
        if isinstance(other, Time):
            return self.time <= other.time
        if isinstance(other, (int, float)):
            return self.time <= other
        return NotImplemented

    def __eq__(self, other: Time | int | float) -> bool:
        """Check equality between Time(s) or with respect to a constant.

        >>> t1 = Time(1)
        >>> t2 = Time(2)
        >>> t1 == t2
        False
        >>> t1 == 1
        True
        """
        if isinstance(other, Time):
            return self.time == other.time
        if isinstance(other, (int, float)):
            return self.time == other
        return NotImplemented

    def __ne__(self, other: Time | int | float) -> bool:
        """Check inequality between Time(s) or with respect to a constant.

        >>> t1 = Time(1)
        >>> t2 = Time(2)
        >>> t1 != t2
        True
        >>> t1 != 1
        False
        """
        return not self == other

    def __gt__(self, other: Time | int | float) -> bool:
        """Compares Time instances.

        >>> t1 = Time(1)
        >>> t2 = Time(2)
        >>> t1 > t2
        False
        >>> t1 < 0
        False
        """
        return not self < other

    def __ge__(self, other: Time | int | float) -> bool:
        """Compares Time instances.

        >>> t1 = Time(1)
        >>> t2 = Time(2)
        >>> t1 >= t2
        False
        >>> t1 >= 1
        True
        """
        return not self <= other

    def __hash__(self) -> int:
        """Return hash value of the given instance."""
        return hash(self.time)

    def __bool__(self) -> bool:
        """Check if Time is null."""
        return Time.time == 0

    def __repr__(self) -> str:
        """Returns a representation of a Time object.

        >>> t = Time(1)
        >>> t
        Time(1)
        """
        return f"{self.__class__.__name__}({self.time})"

    def __str__(self) -> str:
        """Returns a string representation of a Time object.

        >>> t = Time(1)
        >>> print(t)
        Time(1)
        """
        return f"{self.__class__.__name__}({self.time})"


class TimeList(TypeCheckedList):
    """Type checked list of Time instances.

    >>> times = TimeList([])
    >>> times
    TimeList([])

    Implement a load() method for loading times from an iterator (for example from a .csv file row iterator).
    """

    def __init__(self, iterator_arg: list[Time] = None) -> None:
        """
        ---

        iterator_arg : List[Time], optional, default to None
            List of Time instances
        """
        # Initialize the parent class to type check for Time instances
        super().__init__(iterator_arg=iterator_arg, instance_type=Time)

    @classmethod
    def from_json(cls, json_dict: CustomJSONDict) -> TimeList:

        return cls(json_dict["data"])

    def load(self, row_iter: Iterable[dict[str, Any]]) -> None:
        """Load Time instances into the type checked list.

        Parameters
        ----------
        row_iter : Iterator[dict[str, Any]]
            Iterator generating a dictionary dict[str, Any] with key {'time'}.
            For example, the row-iterator of a .csv file.

        Returns
        -------
            A type checked list populated with Vector vectors
        """

        for row in row_iter:

            self.append(Time(row["time"]))

        return None


class TimeListLoader:
    """Loads times into a type-checked list given the column name corresponding to the time values,.

     as stored in the input file.

    >>> source = Path.cwd() / "data" / "sub1.csv"
    >>> usecols = ['time']
    >>> times_loader = TimeListLoader(source, usecols)
    >>> times = times_loader.load()
    >>> times[:3]
    TimeList([Time(1651585280.77981),
             Time(1651585280.78481),
             Time(1651585280.78981)])

    The time, as given by the column name, is automatically re-named to pre-defined name: 'time'

    >>> times[0].time
    1651585280.77981
    """

    # Pre-defined time name
    new_colnames = ["time"]

    def __init__(self, source: Path, usecols: list[str]) -> None:
        """
        ---

            source : Path, required
                Path of the input file.

            usecols : List or Tuple, required
                Names corresponding to the time values as stored in the input file.
        """
        self.source = source
        self.usecols = usecols

        # Map given time name to pre-defined name
        self.col_map_dict = dict(zip(self.usecols, self.new_colnames))

    def load(self) -> TimeList:
        """Loads times into the type checked list from .csv file.

        Returns
        -------
            A type checked list populated with times.
        """
        times = TimeList()
        csv_reader = CSVReader(self.source)
        row_iter = csv_reader.row_iter(
            usecols=self.usecols, col_map_dict=self.col_map_dict
        )
        times.load(row_iter)

        return times
