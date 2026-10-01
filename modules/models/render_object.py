from dataclasses import dataclass
import math

@dataclass
class RenderObject:
    nama: str
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    material_id: int = 0
    transparan: bool = False
    jarak: float = 0.0  # Nanti dihitung secara dinamis dari kamera

    def update_distance(self, camera_x: float, camera_y: float, camera_z: float):
        """Menghitung jarak Euclidean ke posisi kamera."""
        dx = self.x - camera_x
        dy = self.y - camera_y
        dz = self.z - camera_z
        self.jarak = math.sqrt(dx * dx + dy * dy + dz * dz)