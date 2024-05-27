from typing import Any

import numpy as np
from numpy.typing import NDArray


class Circle:
    def __init__(
        self,
        radius: float = 0.0,
        speed: float = 0.0,
        angle_i: float = 0.0,
        angles: NDArray[np.float64] | None = None,
    ) -> None:
        self.radius = radius
        self.speed = speed
        self.angle_i = angle_i
        self._angles: NDArray[np.float64] = np.empty((0,), dtype=np.float64)
        self._local_x: NDArray[np.float64] = np.empty((0,), dtype=np.float64)
        self._local_y: NDArray[np.float64] = np.empty((0,), dtype=np.float64)
        if angles is None:
            self._angles = np.empty((0,), dtype=np.float64)
        else:
            self._angles = angles

    @property
    def local_trajectory(self) -> NDArray[np.float64]:
        return np.stack([self._local_x, self._local_y])

    @property
    def angles(self) -> NDArray[np.float64]:
        return self._angles

    @angles.setter
    def angles(self, value: Any) -> None:
        raise AttributeError(
            "Cannot set angles directly. Set new time array to update."
        )

    @property
    def local_x(self) -> NDArray[np.float64]:
        return self._local_x

    @local_x.setter
    def local_x(self, value: Any) -> None:
        raise AttributeError(
            "Cannot set local_x directly. Set new time array to update."
        )

    @property
    def local_y(self) -> NDArray[np.float64]:
        return self._local_y

    @local_y.setter
    def local_y(self, value: Any) -> None:
        raise AttributeError(
            "Cannot set local_y directly. Set new time array to update."
        )

    def update_arrays(self, time: NDArray[np.float64]) -> None:
        if isinstance(time, np.ndarray) and len(time.shape) == 1:
            self._angles = time * self.speed + self.angle_i
            self._local_x = self.radius * np.cos(self._angles)
            self._local_y = self.radius * np.sin(self._angles)
        else:
            raise ValueError(
                "Time must be set to numpy NDArray of shape (n,)."
            )


class Epicycle:
    def __init__(self) -> None:
        self._circles: list[Circle] = []
        self._time: NDArray[np.float64] = np.empty((0,), dtype=np.float64)
        self._x: NDArray[np.float64] = np.empty((0,), dtype=np.float64)
        self._y: NDArray[np.float64] = np.empty((0,), dtype=np.float64)
        self._period_changed = True
        self._trajectory_changed = True
        self._period: float = 0.0
        self._trajectory: NDArray[np.float64] = np.empty(
            (0,), dtype=np.float64
        )

    @property
    def time(self) -> NDArray[np.float64] | None:
        return self._time

    @time.setter
    def time(self, value: Any) -> None:
        if isinstance(value, np.ndarray) and len(value.shape) == 1:
            self._time = value.astype(np.float64)
            self._x = np.zeros_like(self._time)
            self._y = np.zeros_like(self._time)
            for circle in self._circles:
                circle.update_arrays(self._time)
            self._update_xy()
        else:
            raise ValueError("Time must be set to numpy NDArray or None.")

    @property
    def trajectory(self) -> NDArray[np.float64]:
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
        self, radius: float = 0.0, speed: float = 0.0, angle_i: float = 0.0
    ) -> None:
        self._circles.append(Circle(radius, speed, angle_i, self._time))
        self._period_changed = True
        self._trajectory_changed = True

    def add_circles(
        self, radius: list[float], speed: list[float], angle_i: list[float]
    ) -> None:
        if len(radius) != len(speed) != len(angle_i):
            raise ValueError("Input lists must all have the same shape (n,).")
        for i in range(len(radius)):
            self.add_circle(radius[i], speed[i], angle_i[i])
        self._update_xy()

    def _update_xy(self) -> None:
        self._x = np.zeros_like(self._time)
        self._y = np.zeros_like(self._time)
        for circle in self._circles:
            self._x += circle.local_x
            self._y += circle.local_y
        self._trajectory_changed = True

    @property
    def period(self) -> float:
        if self._period_changed:
            speeds = [circle.speed for circle in self._circles]
            self._period = (
                2 * np.pi / np.lcm.reduce(np.array(speeds, dtype=int))
            )
            self._period_changed = False

        return self._period
