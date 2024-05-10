from numpy.typing import NDArray

from project.core.geometry import Transform


class SVGEncoder:
    @staticmethod
    def encode_path(
        a: NDArray, width: float = 10.0, height: float = 10.0
    ) -> str:
        arr = Transform(a).translate(1, 1).scale(50 * width, 50 * height).a

        out = ""
        out += SVGEncoder.header(width, height)

        path = f"\n    M {arr[0, 0]} {arr[1, 0]} \n"
        for i in range(1, arr.shape[1]):
            path += f"    L {arr[0, i]} {arr[1, i]} \n"

        out += (
            f'  <path d="{path}    "\n'
            + '        fill="none" stroke="black" stroke-width="1" />\n'
        )

        out += "</svg>\n"

        return out

    @staticmethod
    def header(width: float = 10.0, height: float = 10.0) -> str:
        return (
            '<?xml version="1.0" standalone="no"?>\n'
            + '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
            + '  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
            + f'<svg width="{width}cm" height="{height}cm"'
            + f'    viewBox="0 0 {int(width*100)} {int(height*100)}"\n'
            + '     version="1.1" xmlns="http://www.w3.org/2000/svg">\n'
        )


if __name__ == "__main__":
    import numpy as np

    from project.core.geometry import Spirograph

    t = Spirograph.angles(0, 20 * np.pi, 10000)
    spiro = Spirograph.trajectory(0.75, 0.3, t)
    svg = SVGEncoder.encode_path(spiro, width=10, height=10)
    with open("test.svg", "w", encoding="utf-8") as f:
        f.write(svg)
