import math
import pytest
from modules.models.render_object import RenderObject
from modules.culling import CameraFrustum, cull_objects


def test_render_object_3d_distance():
    # Objek di posisi (3, 4, 0)
    obj = RenderObject(nama="Patung", x=3.0, y=4.0, z=0.0)
    
    # Kamera di (0, 0, 0) -> Jarak Pythagoras: sqrt(3^2 + 4^2) = 5.0
    obj.update_distance(0.0, 0.0, 0.0)
    assert obj.jarak == pytest.approx(5.0)


def test_dynamic_camera_movement():
    camera = CameraFrustum(x=0.0, y=0.0, z=0.0, near_plane=1.0, far_plane=10.0)
    obj = RenderObject(nama="Kotak", x=0.0, y=0.0, z=5.0) # Jarak awal = 5.0m (Visible)

    visible = cull_objects([obj], camera)
    assert len(visible) == 1

    # Pindahkan kamera menjauh ke z = -50.0 -> Jarak objek ke kamera jadi 55.0m (Harus ter-cull)
    camera.z = -50.0
    visible_after_move = cull_objects([obj], camera)
    assert len(visible_after_move) == 0