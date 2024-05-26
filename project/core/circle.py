from typing import Any

import numpy as np
from numpy.typing import NDArray


class Circle:
    """
    Circle class.
    Holds information about a construction circle for an epicycle.

    Attributes
    ----------
    radius : float
        Radius of the circle.
    speed : float
        Angular velocity of the circle [rad/s].
    angle_i : float
        Initial angle of the circle [rad]. If this circle is the last one
        in the epicycle construction circles, the point on the circumference
        will be the drawing point, otherwise it will be the point
        on which the center of the next circle is located.
    angles : NDArray
        Numpy array (1, n) of the range of angles [rad].
    local_x : NDArray
        Numpy array (1, n) of x positions with respect to the circle center.
    local_y : NDArray
        Numpy array (1, n) of y positions with respect to the circle center.
    trajectory : NDArray
        Numpy array (2, n) containing the local trajectory of the circle.
    """

    def __init__(
        self,
        radius: int = 0,
        speed: int = 0,
        angle_i=0,
        angles: NDArray | None = None,
    ) -> None:
        self.radius = radius
        self.speed = speed
        self.angle_i = angle_i
        self._angles = np.empty((0,))
        self._local_x = np.empty((0,))
        self._local_y = np.empty((0,))
        if angles is None:
            self._angles = np.empty((0,))
        else:
            self._angles = angles

    @property
    def local_trajectory(self) -> NDArray:
        return np.stack([self._local_x, self._local_y])

    @property
    def angles(self) -> NDArray:
        return self._angles

    @angles.setter
    def angles(self, value: Any) -> None:
        raise AttributeError(
            "Cannot set angles directly. Set new time array to update."
        )

    @property
    def local_x(self) -> NDArray:
        return self._local_x

    @local_x.setter
    def local_x(self, value: Any) -> None:
        raise AttributeError(
            "Cannot set local_x directly. Set new time array to update."
        )

    @property
    def local_y(self) -> NDArray:
        return self._local_y

    @local_y.setter
    def local_y(self, value: Any) -> None:
        raise AttributeError(
            "Cannot set local_y directly. Set new time array to update."
        )

    def update_arrays(self, time: NDArray) -> None:
        """
        Function to update Circle with new time range.

        Parameters
        ----------
        time : NDArray
            Numpy array with new time range.
        """
        if isinstance(time, np.ndarray) and len(time.shape) == 1:
            self._angles = time * self.speed + self.angle_i
            self._local_x = self.radius * np.cos(self._angles)
            self._local_y = self.radius * np.sin(self._angles)
        else:
            raise ValueError(
                "Time must be set to numpy NDArray of shape (n,)."
            )
