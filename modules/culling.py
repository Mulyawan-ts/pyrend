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
    """Filter objek yang berada di dalam pandangan kamera."""
    visible = []
    for obj in objects:
        # Hitung jarak 3D jika koordinat X, Y, atau Z diisi
        if obj.x != 0.0 or obj.y != 0.0 or obj.z != 0.0:
            obj.update_distance(camera.x, camera.y, camera.z)

        if camera.is_visible(obj):
            visible.append(obj)

    return visible