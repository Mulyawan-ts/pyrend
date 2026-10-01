import pytest
from modules.models.render_object import RenderObject
from modules.vector_math import calculate_distances_numpy


def test_numpy_distance_calculation():
    objects = [
        RenderObject(nama="Obj_A", x=3.0, y=4.0, z=0.0),  # Jarak = 5.0
        RenderObject(nama="Obj_B", x=0.0, y=0.0, z=10.0), # Jarak = 10.0
    ]

    # Kamera di (0, 0, 0)
    calculate_distances_numpy(objects, 0.0, 0.0, 0.0)

    assert objects[0].jarak == pytest.approx(5.0)
    assert objects[1].jarak == pytest.approx(10.0)