from typing import Any

import numpy as np
from numpy.typing import NDArray

from project.core.circle import Circle


class Epicycle:
    def __init__(self) -> None:
        self._circles: list[Circle] = []
        self._time: NDArray = np.empty((0,))
        self._x: NDArray = np.empty((0,))
        self._y: NDArray = np.empty((0,))
        self._period_changed = True
        self._trajectory_changed = True
        self._period: float
        self._trajectory: NDArray

    @property
    def time(self) -> NDArray | None:
        return self._time

    @time.setter
    def time(self, value: Any) -> None:
        if isinstance(value, np.ndarray) and len(value.shape) == 1:
            self._time = value
            self._x = np.zeros_like(self._time)
            self._y = np.zeros_like(self._time)
            for circle in self._circles:
                circle.update_arrays(self._time)
                self._x += circle.local_x
                self._y += circle.local_y
        else:
            raise ValueError("Time must be set to numpy NDArray or None.")

    @property
    def trajectory(self) -> NDArray:
        if self._trajectory_changed:
            self._trajectory = np.stack(
                [self._x, self._y, np.ones_like(self._time)]
            )
            self._trajectory_changed = False

        return self._trajectory

    @trajectory.setter
    def trajectory(self) -> None:
        raise AttributeError(
            "Cannot set trajectory directly. Set new time array to update."
        )

    def add_circle(
        self, radius: int = 0, speed: int = 0, angle_i: int = 0
    ) -> None:
        """
        Function to add a new construction circle to the Epicycle.

        Parameters
        ----------
        radius : int
            Radius of the circle.
        speed : int
            Angular velocity of the circle [rad/s].
        angle_i : int
            Initial angle of the circle [rad].
        """
        self._circles.append(Circle(radius, speed, angle_i, self._time))
        self._period_changed = True
        self._trajectory_changed = True

    def add_circles(
        self, radius: list[int], speed: list[int], angle_i: list[int]
    ) -> None:
        if len(radius) != len(speed) != len(angle_i):
            raise ValueError("Input lists must all have the same shape (n,).")
        for i in range(len(radius)):
            self.add_circle(radius[i], speed[i], angle_i[i])
        self.update_arrays()

    def update_arrays(self) -> None:
        self._x = np.zeros_like(self._time)
        self._y = np.zeros_like(self._time)
        for circle in self._circles:
            self._x += circle.local_x
            self._y += circle.local_y

    @property
    def period(self) -> float:
        if self._period_changed:
            speed: list[float] = []

            for circle in self._circles:
                speed.append(circle.speed)

            self._period = 2 * np.pi / np.lcm.reduce(speed)
            self._period_changed = False

        return self._period
