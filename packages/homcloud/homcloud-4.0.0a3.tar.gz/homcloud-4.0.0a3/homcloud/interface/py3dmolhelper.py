import numpy as np
import numbers


def ary2v3(ary):
    return {"x": ary[0], "y": ary[1], "z": ary[2]}


def add_edges(view, edges, color, radius, alpha=1.0):
    assert isinstance(color, str)
    assert isinstance(radius, numbers.Real)
    assert isinstance(alpha, numbers.Real)

    for edge in edges:
        view.addCylinder(
            {"start": ary2v3(edge[0]), "end": ary2v3(edge[1]), "color": color, "radius": radius, "alpha": alpha}
        )


def add_surface(view, triangles, color, alpha=1.0):
    assert isinstance(color, str)
    assert isinstance(alpha, numbers.Real)

    for cell in triangles:
        normal = ary2v3(np.cross(np.array(cell[1]) - cell[0], np.array(cell[2]) - cell[0]))
        view.addCustom(
            {
                "vertexArr": [ary2v3(cell[0]), ary2v3(cell[1]), ary2v3(cell[2])],
                "normalArr": [normal, normal, normal],
                "faceArr": [0, 1, 2],
                "color": color,
                "alpha": alpha,
            }
        )
