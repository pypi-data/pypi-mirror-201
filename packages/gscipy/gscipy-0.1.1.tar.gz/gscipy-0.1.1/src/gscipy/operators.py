"""Module with operators transforming trajectories objects."""
from __future__ import annotations

__author__ = "Matteo Gabba"
__copyright__ = "Copyright 2022, all right reserved Gabba Scientific"
__status__ = "Development"

from abc import ABC, abstractmethod

import numpy as np

from gscipy.time import Time, TimeList
from gscipy.trajectories import BaseTrajectoryCollection, Trajectory
from gscipy.signals import refill_gaps, central_diff, wavelet_filter
from gscipy.vectors import Vector, VectorsList

# TODO: evaluate if to remove __call__
# TODO: evaluate weather adding a transformation_function() method to the BaseOperator class
#  where the transformation logic can be stored as well as other methods required by it
# TODO: define set_params(), get_params() function in Base operator to get/set Operator args after initialization


def _reconstruct_trajectory(
    x: np.ndarray, y: np.ndarray, z: np.ndarray, time: np.ndarray
) -> Trajectory:
    vectors = VectorsList()
    times = TimeList()

    n = len(x)
    for i in range(n):
        r = {"x": x[i], "y": y[i], "z": z[i]}

        vector_i = Vector(**r)
        time_i = Time(time[i])

        vectors.append(vector_i)
        times.append(time_i)

    return Trajectory(vectors, times)


class BaseTrajectoryOperator(ABC):
    """Represents a mathematical function or operation transforming (mapping) a time-series of 3D vectors."""

    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        # Instantiate args and kwargs
        # self.args = args, self.kwargs = kwargs
        ...

    @abstractmethod
    def transform(
        self, trajectory: Trajectory
    ) -> Trajectory | BaseTrajectoryCollection:
        """Implement logic to transform trajectory."""
        ...

        # Template transformation logic for Trajectory:
        # x, y, z, time =  fun(trajectory, *self.args, **self.kwargs)
        # transformed_trajectory = _reconstruct_trajectory(x, y, z, time)
        # return transformed_trajectory

    def __call__(
        self, signal: Trajectory
    ) -> Trajectory | BaseTrajectoryCollection:
        return self.transform(signal)

    def __repr__(self) -> str:
        pars = ", ".join(
            f"{key}={value}" for key, value in self.__dict__.items()
        )
        return f"{self.__class__.__name__}({pars})"


class VectorFirstDiff(BaseTrajectoryOperator):
    def __init__(self, kernel_half_size: int = 1) -> None:
        self.kernel_half_size = kernel_half_size

    def transform(self, trajectory: Trajectory) -> Trajectory:
        # Transformation logic
        delta_x = central_diff(
            trajectory.x, kernel_half_size=self.kernel_half_size
        )
        delta_y = central_diff(
            trajectory.y, kernel_half_size=self.kernel_half_size
        )
        delta_z = central_diff(
            trajectory.z, kernel_half_size=self.kernel_half_size
        )
        time = trajectory.time

        dr = _reconstruct_trajectory(delta_x, delta_y, delta_z, time)

        return dr


class TimeFirstDiff(BaseTrajectoryOperator):
    def __init__(self, kernel_half_size: int = 1) -> None:
        self.kernel_half_size = kernel_half_size

    def transform(self, trajectory: Trajectory) -> Trajectory:
        # Transformation logic
        x = np.ones_like(trajectory.x)
        y = np.ones_like(trajectory.y)
        z = np.ones_like(trajectory.z)
        delta_t = central_diff(
            trajectory.time, kernel_half_size=self.kernel_half_size
        )

        delta_time = _reconstruct_trajectory(x, y, z, delta_t)

        return delta_time


class TimeDerivative(BaseTrajectoryOperator):
    def __init__(self, kernel_half_size: int = 1):
        self.kernel_half_size = kernel_half_size

    def transform(self, trajectory: Trajectory) -> Trajectory:
        delta_position = VectorFirstDiff(self.kernel_half_size)
        delta_time = TimeFirstDiff(self.kernel_half_size)

        delta_r = delta_position(trajectory)
        delta_t = delta_time(trajectory)

        # Transformation logic
        velocity_x = delta_r.x / delta_t.time
        velocity_y = delta_r.y / delta_t.time
        velocity_z = delta_r.z / delta_t.time
        time = delta_r.time

        velocity = _reconstruct_trajectory(
            velocity_x, velocity_y, velocity_z, time
        )

        return velocity


class WaveletFilter(BaseTrajectoryOperator):
    def __init__(
        self,
        wavelet_type: str,
        extension_mode: str,
        filtered_levels: tuple[int, ...],
    ) -> None:
        self.wavelet_type = wavelet_type
        self.extension_mode = extension_mode
        self.filtered_levels = filtered_levels

    def transform(self, trajectory: Trajectory) -> Trajectory:
        args = (self.wavelet_type, self.extension_mode, self.filtered_levels)

        x_filtered, _ = wavelet_filter(trajectory.x, *args)
        y_filtered, _ = wavelet_filter(trajectory.y, *args)
        z_filtered, _ = wavelet_filter(trajectory.z, *args)
        time = trajectory.time

        r_filtered = _reconstruct_trajectory(
            x_filtered, y_filtered, z_filtered, time
        )

        return r_filtered


class RefillGaps(BaseTrajectoryOperator):
    def __init__(self, max_lag: int = 10) -> None:
        self.max_lag = max_lag

    def transform(self, trajectory: Trajectory) -> Trajectory:
        x_refilled = refill_gaps(trajectory.x, self.max_lag)
        y_refilled = refill_gaps(trajectory.y, self.max_lag)
        z_refilled = refill_gaps(trajectory.z, self.max_lag)
        time = trajectory.time

        r_refilled = _reconstruct_trajectory(
            x_refilled, y_refilled, z_refilled, time
        )

        return r_refilled


class SequentialPipeline(BaseTrajectoryOperator):
    """Process the input trajectory sequentially using a list of Operator(s) instances."""

    def __init__(self, steps: list[BaseTrajectoryOperator]) -> None:
        self.steps = steps

    def transform(self, trajectory: Trajectory) -> Trajectory:
        transformed_trajectory = trajectory

        for operator in self.steps:
            transformed_trajectory = operator.transform(transformed_trajectory)

        return transformed_trajectory

    def __getitem__(self, index):
        """Get single operator (by indexing) or sub-pipeline (by slicing)."""
        if isinstance(index, slice):
            return SequentialPipeline(self.steps[index])
        elif isinstance(index, int):
            return self.steps[index]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(steps={[operator for operator in self.steps]})"


class ParallelPipeline(BaseTrajectoryOperator):
    """Process one input trajectory to many output trajectories using a list of Operator(s) instances."""

    def __init__(self, operators: list[BaseTrajectoryOperator]) -> None:
        self.operators = operators

    def transform(self, trajectory: Trajectory) -> list[Trajectory]:

        trajectories = [trajectory]

        for operator in self.operators:
            transformed_trajectory = operator.transform(trajectory)
            trajectories.append(transformed_trajectory)

        return trajectories

    def __getitem__(self, index):
        """Get single operator (by indexing) or sub-pipeline (by slicing)."""
        if isinstance(index, slice):
            return ParallelPipeline(self.operators[index])
        elif isinstance(index, int):
            return self.operators[index]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(operators={[operator for operator in self.operators]})"


class NthVectorDiff(SequentialPipeline):
    def __init__(self, kernel_half_size: int = 1, order: int = 1):

        pipeline_steps = [
            VectorFirstDiff(kernel_half_size) for _ in range(order)
        ]
        super().__init__(pipeline_steps)


class NthTimeDerivative(SequentialPipeline):
    def __init__(self, kernel_half_size: int = 1, order: int = 1):

        pipeline_steps = [
            TimeDerivative(kernel_half_size) for _ in range(order)
        ]
        super().__init__(pipeline_steps)


class DeltaR(NthVectorDiff):
    def __init__(self, kernel_half_size: int = 1):
        super().__init__(kernel_half_size, order=1)


class DeltaDeltaR(NthVectorDiff):
    def __init__(self, kernel_half_size: int = 1):
        super().__init__(kernel_half_size, order=2)


class Velocity(NthTimeDerivative):
    def __init__(self, kernel_half_size: int = 1):
        super().__init__(kernel_half_size, order=1)


class Acceleration(NthTimeDerivative):
    def __init__(self, kernel_half_size: int = 1):
        super().__init__(kernel_half_size, order=2)
