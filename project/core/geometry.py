import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


def n_polygon(n: int) -> NDArray:
    """
    Calculate the vertices locations (on the unit circle)
    of an n-sided polygon.

    Parameters
    ----------
    n : int
        Number of sides.

    Returns
    -------
    NDArray : Polygon vertices of shape (3xn) since
    homogeneous coordinates are used.
    """
    angles = np.linspace(0, 2 * np.pi, n + 1)
    return np.stack([np.cos(angles), np.sin(angles), np.ones_like(angles)])


class Spirograph:

    @staticmethod
    def trajectory(l_r: float, k_r: float, t: NDArray) -> NDArray:
        """
        Calculate spirograph trajectory

        Parameters
        ----------
        l_r : float
            Ratio between drawing point on smaller circle and radius of
            smaller circle (rho/r), physically must be smaller than 1.
        k_r : float
            Ratio between radius of small circle
            to stationary circle (r/R, R=1).
        t : NDArray
            Discretization of angle t.

        Returns
        -------
        NDArray : Spirograph trajectory of shape (3xn) since
        homogeneous coordinates are used.
        """
        xp = (1 - k_r) * np.cos(t) + l_r * k_r * np.cos((1 - k_r) / k_r * t)
        yp = (1 - k_r) * np.sin(t) - l_r * k_r * np.sin((1 - k_r) / k_r * t)
        return np.stack([xp, yp, np.ones_like(t)])

    @staticmethod
    def angles(ti: float, tf: float, steps: int) -> NDArray:
        """
        Calculate spirograph angles discretization.

        Parameters
        ----------
        ti : float
            Initial angle t (between segment connecting
            the two circles centers and x-axis).
        tf : float
            Final angle t.
        steps : int
            Number of steps in the angle t discretization.

        Returns
        -------
        NDArray : Discretization of angle t.
        """
        return np.linspace(ti, tf, steps)


class Transform:
    """
    Class used to perform transformations on an array of points.

    Attributes
    ----------
    a : NDArray
        Input array, must be of shape (3xn) since
        homogeneous coordinates are used.
    """

    def __init__(self, a: NDArray) -> None:
        Transform.check_input(a)
        self.a = np.copy(a)

    def translate(self, tx: float, ty: float) -> "Transform":
        """
        Method for translating an array of points.

        Returns
        -------
        Transform
            The method returns itself so that multiple
            transformations can be applied at once.

        See Also
        --------
        _translate : Contains attribute definitions.
        """
        self.a = Transform._translate(self.a, tx, ty)
        return self

    def rotate(self, r: float) -> "Transform":
        """
        Method for rotating an array of points about the origin.

        Returns
        -------
        Transform
            The method returns itself so that multiple
            transformations can be applied at once.

        See Also
        --------
        _rotate : Contains attribute definitions.
        """
        self.a = Transform._rotate(self.a, r)
        return self

    def scale(self, sx: float, sy: float) -> "Transform":
        """
        Method for scaling an array of points about the origin.

        Returns
        -------
        Transform
            The method returns itself so that multiple
            transformations can be applied at once.

        See Also
        --------
        _scale : Contains attribute definitions.
        """
        self.a = Transform._scale(self.a, sx, sy)
        return self

    def rotate_p(self, r: float, px: float, py: float) -> "Transform":
        """
        Method for rotating an array of points
        about an arbitrary pivot point P.

        Returns
        -------
        Transform
            The method returns itself so that multiple
            transformations can be applied at once.

        See Also
        --------
        _rotate_p : Contains attribute definitions.
        """
        self.a = Transform._rotate_p(self.a, r, px, py)
        return self

    def scale_p(
        self, sx: float, sy: float, px: float, py: float
    ) -> "Transform":
        """
        Method for scaling an array of points
        about an arbitrary pivot point P.

        Returns
        -------
        Transform
            The method returns itself so that multiple
            transformations can be applied at once.

        See Also
        --------
        _scale_p : Contains attribute definitions.
        """
        self.a = Transform._scale_p(self.a, sx, sy, px, py)
        return self

    @staticmethod
    def _translate(a: NDArray, tx: float, ty: float) -> NDArray:
        """
        Protected method for translating an array of points.

        Parameters
        ----------
        a : NDArray
            Input array, must be of shape (3xn) since
            homogeneous coordinates are used.
        tx : float
            Translation in x direction.
        ty : float
            Translation in y direction.

        Returns
        -------
        NDArray
            Output array of shape (3xn) since
            homogeneous coordinates are used.
        """
        return np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]]) @ a

    @staticmethod
    def _rotate(a: NDArray, r: float) -> NDArray:
        """
        Protected method for rotating an array of points about the origin.

        Parameters
        ----------
        a : NDArray
            Input array, must be of shape (3xn) since
            homogeneous coordinates are used.
        r : float
            Rotation in radians.

        Returns
        -------
        NDArray
            Output array of shape (3xn) since
            homogeneous coordinates are used.
        """
        return (
            np.array(
                [
                    [np.cos(r), -np.sin(r), 0],
                    [np.sin(r), np.cos(r), 0],
                    [0, 0, 1],
                ]
            )
            @ a
        )

    @staticmethod
    def _scale(a: NDArray, sx: float, sy: float) -> NDArray:
        """
        Protected method for scaling an array of points about the origin.

        Parameters
        ----------
        a : NDArray
            Input array, must be of shape (3xn) since
            homogeneous coordinates are used.
        sx : float
            Scaling factor in x direction.
        sy : float
            Scaling factor in y direction.

        Returns
        -------
        NDArray
            Output array of shape (3xn) since
            homogeneous coordinates are used.
        """
        return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]]) @ a

    @staticmethod
    def _rotate_p(a: NDArray, r: float, px: float, py: float) -> NDArray:
        """
        Protected method for rotating an array of points
        about an arbitrary pivot point P.

        Parameters
        ----------
        a : NDArray
            Input array, must be of shape (3xn) since
            homogeneous coordinates are used.
        r : float
            Rotation in radians.
        px : float
            x coordinate of the pivot point P.
        py : float
            y coordinate of the pivot point P.

        Returns
        -------
        NDArray
            Output array of shape (3xn) since
            homogeneous coordinates are used.
        """
        return Transform._translate(
            Transform._rotate(Transform._translate(a, -px, -py), r), px, py
        )

    @staticmethod
    def _scale_p(
        a: NDArray, sx: float, sy: float, px: float, py: float
    ) -> NDArray:
        """
        Protected method for scaling an array of points
        about an arbitrary pivot point P.

        Parameters
        ----------
        a : NDArray
            Input array, must be of shape (3xn) since
            homogeneous coordinates are used.
        sx : float
            Scaling factor in x direction.
        sy : float
            Scaling factor in y direction.
        px : float
            x coordinate of the pivot point P.
        py : float
            y coordinate of the pivot point P.

        Returns
        -------
        NDArray
            Output array of shape (3xn) since
            homogeneous coordinates are used.
        """
        return Transform._translate(
            Transform._scale(Transform._translate(a, -px, -py), sx, sy), px, py
        )

    @staticmethod
    def check_input(a: NDArray) -> None:
        if a.shape[0] != 3:
            raise ValueError("Input array must be of shape (3xn)")


if __name__ == "__main__":
    # polygon = n_polygon(3)
    # polygon = Transform.rotate(polygon, np.pi / 4)
    # polygon = Transform.translate(polygon, 1, 2)
    # polygon = Transform(polygon).rotate_p(np.pi / 4, 1, 0).a
    # print(polygon)
    # plt.plot(polygon[0, :], polygon[1, :])

    l_r = 0.8
    k_r = 0.67

    steps = 1000

    t = Spirograph.angles(0, 2 * np.pi, steps)
    spiro = Spirograph.trajectory(l_r, k_r, t)
    # plt.plot(spiro_x, spiro_y)

    # plt.gca().set_aspect("equal", adjustable="box")
    # plt.show()

    c_x = (1 - k_r) * np.cos(t)
    c_y = (1 - k_r) * np.sin(t)

    c1 = plt.Circle((0, 0), 1, fill=False)
    c2 = plt.Circle((c_x[0], c_y[0]), k_r, fill=False)

    fig, ax = plt.subplots()
    ax.add_patch(c1)
    ax.add_patch(c2)
    dl = ax.plot([c_x[0], spiro[0, 0]], [c_y[0], spiro[1, 0]], color="black")[
        0
    ]
    line = ax.plot(spiro[0, 0], spiro[1, 0])[0]
    ax.set(xlim=[-1, 1], ylim=[-1, 1])

    fig.gca().set_aspect("equal", adjustable="box")

    def update(frame):
        c2.set_center((c_x[frame], c_y[frame]))
        dl.set_xdata([c_x[frame], spiro[0, frame]])
        dl.set_ydata([c_y[frame], spiro[1, frame]])
        # update the line plot:
        line.set_xdata(spiro[0, :frame])
        line.set_ydata(spiro[1, :frame])
        return line

    ani = animation.FuncAnimation(
        fig=fig, func=update, frames=steps, interval=10
    )
    plt.show()
