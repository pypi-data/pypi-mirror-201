"""Module for creation (and handling) of multidimensional vectors and trajectories."""
from __future__ import annotations

__author__ = "Matteo Gabba"
__copyright__ = "Copyright 2022, all right reserved Gabba Scientific"
__status__ = "Development"

from abc import abstractmethod
from collections.abc import Collection, Iterator
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from gscipy.decorators import check_args_len
from gscipy.json_io import CustomJSONDict, JsonIOInterface
from gscipy.time import Time, TimeList, TimeListLoader
from gscipy.vectors import Vector, VectorListLoader, VectorsList

# TODO: create method to perform operations on time axis (invert, sort, rel_to_abs) in Trajectory
# TODO: create decorator to check type hinting of input args
# TODO: unit test the VectorNDim class


@dataclass(frozen=True)
class Trajectory(JsonIOInterface):
    """Represents a time series of 3D vectors instances.

    A Trajectory instance is instantiated by a list of 3D vectors and the corresponding times, a type error is raised
    otherwise. The two lists must contain the same number of Vector and Time instances.

    >>> source = Path.cwd() / "data" / "sub1.csv"
    >>> time_colnames = ['time']
    >>> coord_colnames = ['gaze_deg_coord_x', 'gaze_deg_coord_y']
    >>> times = TimeListLoader(source, usecols=time_colnames).load()
    >>> vectors = VectorListLoader(source, usecols=coord_colnames).load()
    >>> trajectory = Trajectory(vectors, times)
    >>> trajectory[:3]
    (VectorsList([Vector(0.4622481497169438, 3.76608427632374, 0.0),
                  Vector(0.46393828577858687, 3.7411490072433953, 0.0),
                  Vector(0.456283375837779, 3.7295640810489856, 0.0)]),
     TimeList([Time(1651585280.77981),
               Time(1651585280.78481),
               Time(1651585280.78981)]))

    A Trajectory instance contains the following properties: vector coordinates (x, y, z), vector magnitudes,
     time values, time zero (t0), relative time from start of the time-series:

    >>> trajectory.x[:5]
    array([0.46224815, 0.46393829, 0.45628338, 0.50202114, 0.51964137])
    >>> trajectory.y[:5]
    array([3.76608428, 3.74114901, 3.72956408, 3.70602158, 3.94218248])
    >>> trajectory.z[:5]
    array([0., 0., 0., 0., 0.])

    >>> trajectory.magnitude[:5]
    array([14.18500018, 13.99785081, 13.91120624, 13.73690808, 15.54314845])

    >>> trajectory.time[:5]
    array([1.65158528e+09, 1.65158528e+09, 1.65158528e+09, 1.65158528e+09,
           1.65158528e+09])

    >>> trajectory.t0
    1651585280.77981
    >>> trajectory.rtime[:5]
    array([0.        , 0.00500011, 0.00999999, 0.0150001 , 0.01999998])

    A Trajectory instance supports dot and cross vector products both trajectory-wise

    >>> dot_prod = trajectory.dot(trajectory)
    >>> dot_prod[:3]
    [14.397064128289646, 14.211434627409416, 14.117842753716685]

    >>> cross_prod = trajectory.cross(trajectory)
    >>> cross_prod[:3]
    (VectorsList([Vector(0.0, 0.0, 0.0),
                  Vector(0.0, 0.0, 0.0),
                  Vector(0.0, 0.0, 0.0)]),
     TimeList([Time(1651585280.77981),
               Time(1651585280.78481),

    and by a single vector

    >>> vector = trajectory[0][0]
    >>> vector
    Vector(0.4622481497169438, 3.76608427632374, 0.0)

    >>> dot_prod = trajectory.dot(vector)
    >>> dot_prod[:3]
    [14.397064128289646, 14.303937065747524, 14.256768789407998]
    >>> dot_prod = trajectory @ vector
    >>> dot_prod[:3]
    [14.397064128289646, 14.303937065747524, 14.256768789407998]

    >>> cross_prod = trajectory.cross(vector)
    >>> cross_prod[:3]
    (VectorsList([Vector(0.0, 0.0, 0.0),
                  Vector(0.0, 0.0, 0.01789147684168535),
                  Vector(0.0, 0.0, -0.005582448425092368)]),
     TimeList([Time(1651585280.77981),
               Time(1651585280.78481),
               Time(1651585280.78981)]))

    The following operations are implemented by operator overlaoding

    Get item(s) (Vector, Time) by indexing or slicing
    >>> trajectory[1]
    (Vector(0.46393828577858687, 3.7411490072433953, 0.0), Time(1651585280.78481))
    >>> trajectory[:2]
    (VectorsList([Vector(0.4622481497169438, 3.76608427632374, 0.0),
                  Vector(0.46393828577858687, 3.7411490072433953, 0.0)]),
    TimeList([Time(1651585280.77981), Time(1651585280.78481)]))

    Iteration
    >>> ((vector, time) for (vector, time) in trajectory)
    <generator object <genexpr> at 0x000002D749F9FB50>

    Get the total number of items
    >>> len(trajectory)
    6281

    Vector addition both trajectory-wise or by a single-vector
    >>> add1 = trajectory + trajectory
    >>> add1[:2]
    (VectorsList([Vector(0.9244962994338876, 7.53216855264748, 0.0),
                  Vector(0.9278765715571737, 7.4822980144867905, 0.0)]),
    TimeList([Time(1651585280.77981), Time(1651585280.78481)]))
    >>> add2 = trajectory + vector
    >>> add2[:2]
    (VectorsList([Vector(0.9244962994338876, 7.53216855264748, 0.0),
                  Vector(0.9261864354955307, 7.507233283567135, 0.0)]),
     TimeList([Time(1651585280.77981), Time(1651585280.78481)]))

    Vector subtraction both trajectory-wise or by a single-vector
    >>> sub1 = trajectory - trajectory
    >>> sub1[:2]
    (VectorsList([Vector(0.0, 0.0, 0.0), Vector(0.0, 0.0, 0.0)]),
     TimeList([Time(1651585280.77981), Time(1651585280.78481)]))
    >>> sub2 = trajectory - vector
    >>> sub2[:2]
    (VectorsList([Vector(0.0, 0.0, 0.0),
                  Vector(0.0016901360616430883, -0.024935269080344824, 0.0)]),
    TimeList([Time(1651585280.77981), Time(1651585280.78481)]))

    Coordinate-wise vector multiplication
    >>> mul1 = trajectory * trajectory
    >>> mul1[:2]
    (VectorsList([Vector(0.21367335191673806, 14.183390776372908, 0.0),
                  Vector(0.21523873301117374, 13.996195894398243, 0.0)]),
     TimeList([Time(1651585280.77981), Time(1651585280.78481)]))

    >>> mul2 = trajectory * vector
    >>> mul2[:2]
    (VectorsList([Vector(0.21367335191673806, 14.183390776372908, 0.0),
                  Vector(0.21445461418400247, 14.089482451563521, 0.0)]),
     TimeList([Time(1651585280.77981), Time(1651585280.78481)]))

    Vector scalar multiplication
    >>> mul3 = trajectory * 2
    >>> mul3[:2]
    (VectorsList([Vector(0.9244962994338876, 7.53216855264748, 0.0),
                  Vector(0.9278765715571737, 7.4822980144867905, 0.0)]),
     TimeList([Time(1651585280.77981), Time(1651585280.78481)]))

    Raise to the power of a number
    >>> pow1 = trajectory ** 2
    >>> pow1[:2]
    (VectorsList([Vector(0.21367335191673806, 14.183390776372908, 0.0),
                  Vector(0.21523873301117374, 13.996195894398243, 0.0)]),
     TimeList([Time(1651585280.77981), Time(1651585280.78481)]))

    Inverse vectors
    >>> inv = -trajectory
    >>> inv[:2]
    (VectorsList([Vector(-0.4622481497169438, -3.76608427632374, -0.0),
                  Vector(-0.46393828577858687, -3.7411490072433953, -0.0)]),
     TimeList([Time(1651585280.77981), Time(1651585280.78481)]))

    Absolute values
    >>> abs_val = abs(trajectory)
    >>> abs_val[:2]
    array([14.18500018, 13.99785081])

    Check (in)equality between all items of two Trajectory instances
    >>> trajectory == trajectory
    True
    >>> trajectory != trajectory
    False
    """

    vectors: VectorsList = VectorsList()
    times: TimeList = TimeList()

    @classmethod
    def from_json(cls, json_dict: CustomJSONDict) -> Trajectory:
        return cls(json_dict["vectors"], json_dict["times"])

    def __post_init__(self):
        if not isinstance(self.vectors, VectorsList):
            raise TypeError(
                f"{self.__class__.__name__}() argument 'vector' must be a type-checked list of Vector(s),"
                f" not '{self.vectors.__class__.__name__}'"
            )
        if not isinstance(self.times, TimeList):
            raise TypeError(
                f"{self.__class__.__name__}() argument 'times' must be a type-checked list of Time(s),"
                f" not '{self.times.__class__.__name__}'"
            )
        assert len(self.vectors) == len(self.times), (
            f"Trajectory instance arguments 'vectors' and 'times' must have same dimension, not {len(self.vectors)}"
            f" and {len(self.times)}"
        )

    @property
    def magnitude(self) -> np.ndarray:
        """Magnitudes of Trajectory vectors."""
        return np.array([vector.magnitude for vector in self.vectors])

    @property
    def x(self) -> np.ndarray:
        """X-coordinate of Trajectory vectors."""
        return np.array([vector.x for vector in self.vectors])

    @property
    def y(self) -> np.ndarray:
        """Y-coordinate of Trajectory vectors."""
        return np.array([vector.y for vector in self.vectors])

    @property
    def z(self) -> np.ndarray:
        """Z-coordinate of Trajectory vectors."""
        return np.array([vector.z for vector in self.vectors])

    @property
    def time(self) -> np.ndarray:
        return np.array([time.time for time in self.times])

    @property
    def rtime(self) -> np.ndarray:
        """Relative time from the first point of the time-series."""
        return self.time - self.t0

    @property
    def t0(self) -> float:
        """First point of the time series."""
        return self.time[0]

    @check_args_len
    def dot(self, other: Trajectory | Vector) -> list[float]:
        """Dot product of Trajectory vectors.

        If 'other' is a Trajectory instance the vectors of the two trajectories ('self' and 'other') are multiplied
        element by element.
        If 'other' is a Vector instance all vectors of 'self' are multiplied by the 'other' vector.

        Raise AssertionError if the two trajectories have different dimension.
        Raise TypeError if 'other' is not a Trajectory or Vector instance.

        Returns
        -------
            A list of float values corresponding to the dot products for each vector of the input Trajectory(s).
        """
        if isinstance(other, self.__class__):
            return [r1.dot(r2) for r1, r2 in zip(self.vectors, other.vectors)]
        if isinstance(other, Vector):
            return [r.dot(other) for r in self.vectors]
        raise TypeError(
            f"unsupported operand type(s) for {self.__class__.__name__}.dot():"
            f" '{other.__class__.__name__}'"
        )

    @check_args_len
    def cross(self, other: Trajectory | Vector) -> Trajectory:
        """Cross product of Trajectory vectors.

        If 'other' is a Trajectory instance the vectors of the two trajectories ('self' and 'other') are multiplied
        element by element.
        If 'other' is a Vector instance all vectors of 'self' are multiplied by the 'other' vector.

        Raise AssertionError if the two trajectories have different dimension.
        Raise TypeError if 'other' is not a Trajectory or Vector instance.

        Returns
        -------
            A Trajectory instance corresponding to the cross products for each vector of the input Trajectory(s).
        """
        if isinstance(other, self.__class__):
            return self(
                VectorsList(
                    [
                        r1.cross(r2)
                        for r1, r2 in zip(self.vectors, other.vectors)
                    ]
                ),
                self.times,
            )
        if isinstance(other, Vector):
            return self(
                VectorsList([r.cross(other) for r in self.vectors]),
                self.times,
            )
        raise TypeError(
            f"unsupported operand type(s) for {self.__class__.__name__}.cross():"
            f" '{other.__class__.__name__}'"
        )

    def __call__(self, vectors: VectorsList, times: TimeList) -> Trajectory:
        """Makes Trajectory instance callable."""
        return self.__class__(vectors, times)

    def __getitem__(self, index: int) -> tuple[Vector, Time]:
        """Get Trajectory items (Vector, Time) by index or slicing."""
        return self.vectors[index], self.times[index]

    def __iter__(self) -> Iterator[tuple[Vector, Time]]:
        """Allows iteration over the Trajectory items."""
        return iter(zip(self.vectors, self.times))

    def __len__(self) -> int:
        """Returns Trajectory length (number of items in the time-series)."""
        return len(self.vectors)

    @check_args_len
    def __add__(self, other: Trajectory | Vector) -> Trajectory:
        """Addition of Trajectory vectors.

        If 'other' is a Trajectory instance the vectors of the two trajectories ('self' and 'other') are added
        element by element.
        If 'other' is a Vector instance the 'other' vector is added to all vectors of 'self'.

        Raise AssertionError if the two trajectories have different dimension.
        Raise TypeError if 'other' is not a Trajectory or Vector instance.
        """
        if isinstance(other, self.__class__):
            return self(
                VectorsList(
                    [r1 + r2 for r1, r2 in zip(self.vectors, other.vectors)]
                ),
                self.times,
            )
        if isinstance(other, Vector):
            return self(
                VectorsList([r + other for r in self.vectors]), self.times
            )

        return NotImplemented

    def __radd__(self, other: Trajectory | Vector) -> Trajectory:
        return self + other

    @check_args_len
    def __sub__(self, other: Trajectory | Vector) -> Trajectory:
        """Subtraction of Trajectory vectors.

        If 'other' is a Trajectory instance the vectors of the two trajectories ('self' and 'other') are subtracted
        element by element.
        If 'other' is a Vector instance the 'other' vector is subtracted to all vectors of 'self'.

        Raise AssertionError if the two trajectories have different dimension.
        Raise TypeError if 'other' is not a Trajectory or Vector instance.
        """
        return self + (-other)

    def __rsub__(self, other: Trajectory | Vector) -> Trajectory:
        return other + (-self)

    @check_args_len
    def __mul__(
        self,
        other: Trajectory | Vector | int | float,
    ) -> Trajectory:
        """Coordinate-wise multiplication of Trajectory vectors.

        If 'other' is a Trajectory instance the vectors of the two trajectories ('self' and 'other') are multiplied
        coordinate-wise vector by vector.
        If 'other' is a Vector instance the 'other' vector is multiplied coordinate-wise to all vectors of 'self'.
        If 'other' is a number (float or int) all vectors of 'self' are scalar multiplied by 'other'.

        Raise AssertionError if the two trajectories have different dimension.
        Raise TypeError if 'other' is not a Trajectory, Vector, float or int type.
        """
        if isinstance(other, self.__class__):
            return self(
                VectorsList(
                    [r1 * r2 for r1, r2 in zip(self.vectors, other.vectors)]
                ),
                self.times,
            )
        if isinstance(other, (Vector, int, float)):
            return self(
                VectorsList([r * other for r in self.vectors]), self.times
            )
        return NotImplemented

    def __rmul__(self, other: Trajectory | int | float) -> Trajectory:
        return self * other

    def __matmul__(self, other: Trajectory | Vector) -> list[float]:
        """Overload @ operator with dot product."""
        return self.dot(other)

    def __pow__(self, power: int | float) -> Trajectory:
        """Raise to the power Trajectory vectors."""
        if isinstance(power, (int, float)):
            return self(
                VectorsList([r**power for r in self.vectors]), self.times
            )
        return NotImplemented

    def __neg__(self) -> Trajectory:
        """Inverse of Trajectory vectors."""
        return self(VectorsList([-r for r in self.vectors]), self.times)

    def __pos__(self) -> Trajectory:
        return self

    def __abs__(self) -> np.ndarray:
        """Absolute value (magnitude) of Trajectory vectors."""
        return self.magnitude

    @check_args_len
    def __eq__(self, other: Trajectory) -> bool:
        """Check equality between each item (Vector, Time) of two Trajectory instances."""
        if isinstance(other, self.__class__):
            return (self.vectors == other.vectors) and (
                self.times == other.times
            )
        return NotImplemented

    def __ne__(self, other: Trajectory) -> bool:
        """Check inequality between each item (Vector, Time) of two Trajectory instances."""
        return not self == other

    def __hash__(self) -> int:
        """Return hash value of the given instance."""
        return hash(tuple(self))

    def __bool__(self) -> bool:
        """Check that all vectors and times are null."""
        return all(r == 0 for r, t in self) and all(t == 0 for r, t in self)

    def __repr__(self) -> str:
        """Returns a representation of a Vector object."""
        return f"{self.__class__.__name__}({[(r, t) for r, t in zip(self.vectors, self.times)]})"

    def __str__(self) -> str:
        """Returns a string representation of a Vector object."""
        return f"length={len(self)}, \n{[(r, t) for r, t in zip(self.vectors, self.times)]}"


class TrajectoryLoader:
    """Create a Trajectory instance from file.

    >>> source = Path.cwd() / "data" / "sub1.csv"
    >>> time_colnames = ['time']
    >>> coord_colnames = ['gaze_deg_coord_x', 'gaze_deg_coord_y']
    >>> trajectory_loader = TrajectoryLoader(source, time_colnames, coord_colnames)
    >>> trajectory = trajectory_loader.load()
    >>> trajectory[:2]
    (VectorsList([Vector(0.4622481497169438, 3.76608427632374, 0.0),
                  Vector(0.46393828577858687, 3.7411490072433953, 0.0)]),
     TimeList([Time(1651585280.77981), Time(1651585280.78481)]))
    """

    def __init__(
        self,
        source: Path,
        time_colnames: list[str],
        coord_colnames: list[str],
    ) -> None:
        """
        ---

            source : Path, required
                Path of the file storing the vector coordinates and the corresponding times.

            time_colnames : list[str], required
                Name of the column storing the time values.

            coord_colnames : list[str], required
                Names of the columns storing the 3D coordinates, or a subset of those, of the vectors.
        """
        self.source = source
        self.time_colnames = time_colnames
        self.coord_colnames = coord_colnames

    def load(self) -> Trajectory:
        """
        ---

            A Trajectory instance.
        """
        times = TimeListLoader(self.source, usecols=self.time_colnames).load()
        vectors = VectorListLoader(
            self.source, usecols=self.coord_colnames
        ).load()

        return Trajectory(vectors, times)


@dataclass
class BaseTrajectoryCollection(Collection):
    def __post_init__(self):
        for name, value in self.__dict__.items():
            if not isinstance(value, Trajectory):
                raise TypeError(
                    f"unsupported '{name}' argument type for {self.__class__.__name__}():"
                    f" '{value.__class__.__name__}'"
                )

    def __iter__(self) -> Iterator[tuple[str, Trajectory]]:
        for (name, trajectory) in self.__dict__.items():
            yield name, trajectory

    def __contains__(self, trajectory) -> bool:
        return trajectory in self.__dict__.values()

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(attrs={[key for key in self.__dict__.keys()]})"
