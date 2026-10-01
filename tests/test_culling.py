from modules.vector_math import calculate_distances_numpy


class CameraFrustum:
    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        near_plane: float = 0.1,
        far_plane: float = 100.0,
    ):
        self.x = x
        self.y = y
        self.z = z
        self.near_plane = near_plane
        self.far_plane = far_plane

    def is_visible(self, obj) -> bool:
        return self.near_plane <= obj.jarak <= self.far_plane


def cull_objects(objects, camera):
    if not objects:
        return []

    # Hitung jarak 3D seluruh objek sekaligus dengan NumPy
    calculate_distances_numpy(objects, camera.x, camera.y, camera.z)

    # Filter objek berdasarkan near & far plane
    return [obj for obj in objects if camera.is_visible(obj)]