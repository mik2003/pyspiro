from numpy.typing import NDArray

from project.core.geometry import Transform


class SVGEncoder:
    @staticmethod
    def encode_path(
        a: NDArray, size: float = 10.0, padding: float = 0.5
    ) -> str:
        arr = Transform(a).translate(1, 1).scale(50 * size, 50 * size).a

        out = ""
        out += SVGEncoder.header(size, size, padding)

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
    def header(
        width: float = 10.0, height: float = 10.0, padding: float = 0.5
    ) -> str:
        return (
            '<?xml version="1.0" standalone="no"?>\n'
            + '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
            + '  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
            + f'<svg width="{width+2*padding}cm" height="{height+2*padding}cm"'
            + f'    viewBox="{-int(padding*100)} {-int(padding*100)} '
            + f'{int((width+padding)*100)} {int((height+padding)*100)}"\n'
            + '     version="1.1" xmlns="http://www.w3.org/2000/svg">\n'
        )


if __name__ == "__main__":
    import time

    import numpy as np

    from project.core.epicycle import Epicycle

    # from project.core.geometry import Spirograph

    t_0 = time.time()

    # t = Spirograph.angles(0, 20 * np.pi, 10000)
    # spiro = Spirograph.trajectory(0.75, 0.3, t)
    # svg = SVGEncoder.encode_path(spiro, width=10, height=10)
    # with open("test.svg", "w", encoding="utf-8") as f:
    #     f.write(svg)

    e = Epicycle()
    n = 3
    radius = n * [1]
    speed = [3, 7, 31]  # n * [1]
    angle_i = n * [0]
    e.add_circles(radius / np.sum(radius), speed, angle_i)
    e.time = np.linspace(0, 2 * np.pi, int(60 * np.max(speed)))

    svg = SVGEncoder.encode_path(e.trajectory)
    with open("test.svg", "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Execution time: {(time.time()-t_0)*1000:.1f} ms.")
