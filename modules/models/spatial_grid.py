import numpy as np


class SpatialGrid3D:
    def __init__(self, cell_size: float = 50.0):
        self.cell_size = cell_size
        # Dictionary menyimpan list indeks objek per Cell ID: {cell_id: [idx1, idx2, ...]}
        self.grid = {}

    def _get_cell_coords(self, positions: np.ndarray) -> np.ndarray:
        """Mengubah posisi 3D (N, 3) menjadi koordinat grid 3D (N, 3)."""
        return np.floor(positions / self.cell_size).astype(np.int32)

    def build_grid(self, store):
        """Memasukkan seluruh objek dari DataStore ke dalam Spatial Grid."""
        self.grid.clear()
        n = store.count
        if n == 0:
            return

        cell_coords = self._get_cell_coords(store.positions[:n])

        # Kelompokkan indeks berdasarkan koordinat sel
        for idx, (gx, gy, gz) in enumerate(cell_coords):
            cell_id = (int(gx), int(gy), int(gz))
            if cell_id not in self.grid:
                self.grid[cell_id] = []
            self.grid[cell_id].append(idx)

    def get_candidate_indices(self, camera_pos: np.ndarray, far_plane: float) -> np.ndarray:
        """
        Mengembalikan HANYA indeks objek dari sel-sel yang berada dalam radius far_plane.
        Objek di luar sel ini diabaikan total!
        """
        radius_cells = int(np.ceil(far_plane / self.cell_size))
        cam_gx, cam_gy, cam_gz = np.floor(camera_pos / self.cell_size).astype(np.int32)

        candidate_indices = []

        # Hanya iterasi sel-sel di sekitar kamera
        for dx in range(-radius_cells, radius_cells + 1):
            for dy in range(-radius_cells, radius_cells + 1):
                for dz in range(-radius_cells, radius_cells + 1):
                    cell_id = (cam_gx + dx, cam_gy + dy, cam_gz + dz)
                    if cell_id in self.grid:
                        candidate_indices.extend(self.grid[cell_id])

        if not candidate_indices:
            return np.array([], dtype=int)

        return np.array(candidate_indices, dtype=int)