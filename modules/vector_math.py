import numpy as np
import math


# --- FUNGSI UNTUK DOD (DataStore / NumPy Arrays) ---
def compute_distances_and_cull(store, camera_pos: np.ndarray, near_plane: float, far_plane: float):
    n = store.count
    if n == 0:
        return np.array([], dtype=bool)

    deltas = store.positions[:n] - camera_pos
    store.distances[:n] = np.linalg.norm(deltas, axis=1)

    distances = store.distances[:n]
    visible_mask = (distances >= near_plane) & (distances <= far_plane)

    return visible_mask


# --- FUNGSI UNTUK LEGACY / OOP (List of RenderObject) ---
def calculate_distances_fast(objects, camera_x: float, camera_y: float, camera_z: float):
    for obj in objects:
        dx = obj.x - camera_x
        dy = obj.y - camera_y
        dz = obj.z - camera_z
        obj.jarak = math.hypot(dx, dy, dz)


def calculate_distances_numpy(objects, camera_x: float, camera_y: float, camera_z: float):
    """Alias/pembungkus agar test lama yang menguji NumPy pada RenderObject tetap jalan."""
    if not objects:
        return
    positions = np.array([[obj.x, obj.y, obj.z] for obj in objects], dtype=np.float32)
    camera_pos = np.array([camera_x, camera_y, camera_z], dtype=np.float32)
    deltas = positions - camera_pos
    distances = np.linalg.norm(deltas, axis=1)
    for obj, dist in zip(objects, distances):
        obj.jarak = float(dist)

def compute_distances_and_cull_grid(
    store, candidate_indices: np.ndarray, camera_pos: np.ndarray, near_plane: float, far_plane: float
):
    """
    Culling presisi HANYA untuk objek kandidat yang diambil dari Spatial Grid.
    """
    if len(candidate_indices) == 0:
        return np.array([], dtype=int)

    # 1. Ambil posisi hanya objek kandidat
    candidate_positions = store.positions[candidate_indices]

    # 2. Vectorized Distance hanya pada kandidat
    deltas = candidate_positions - camera_pos
    dists = np.linalg.norm(deltas, axis=1)

    # Simpan balik nilai jarak ke store untuk candidate_indices
    store.distances[candidate_indices] = dists

    # 3. Filter Near & Far Plane
    valid_mask = (dists >= near_plane) & (dists <= far_plane)

    # Kembalikan indeks asli objek yang lolos
    return candidate_indices[valid_mask]