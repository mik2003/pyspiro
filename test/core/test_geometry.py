import numpy as np
import pytest
from numpy.typing import NDArray

from project.core.geometry import Transform

a = np.array([[1], [1], [1]])


@pytest.mark.parametrize(
    "a, r, px, py",
    [
        (a, 0, 0, 0),
        (a, 1, 0, 0),
        (a, 1, 1, 0),
        (a, 1, 0, 1),
        (a, 1, 1, 1),
    ],
)
def test_rotate_p(a: NDArray, r: float, px: float, py: float) -> None:
    np.testing.assert_array_almost_equal(
        Transform._rotate_p(a, r, px, py),
        (
            np.array([[1, 0, px], [0, 1, py], [0, 0, 1]])
            @ np.array(
                [
                    [np.cos(r), -np.sin(r), 0],
                    [np.sin(r), np.cos(r), 0],
                    [0, 0, 1],
                ]
            )
            @ np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]])
            @ a
        ),
    )
