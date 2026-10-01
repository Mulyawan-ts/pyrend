import numpy as np
import pytest
from modules.models.render_data import RenderDataStore
from modules.models.spatial_grid import SpatialGrid3D
from modules.vector_math import compute_distances_and_cull_grid


def test_spatial_grid_culling():
    store = RenderDataStore(capacity=10)
    grid = SpatialGrid3D(cell_size=10.0)

    # 3 Objek: Dekat (z=5), Sedang (z=15), Sangat Jauh (z=500)
    positions = np.array([
        [0.0, 0.0, 5.0],
        [0.0, 0.0, 15.0],
        [0.0, 0.0, 500.0],
    ], dtype=np.float32)

    mats = np.array([1, 1, 2], dtype=np.int32)
    trans = np.array([False, False, False], dtype=bool)

    store.add_objects(positions, mats, trans)
    grid.build_grid(store)

    camera_pos = np.array([0.0, 0.0, 0.0], dtype=np.float32)
    far_plane = 20.0  # Hanya melihat radius 20m

    # 1. Ambil kandidat dari Grid (Objek z=500 tidak akan terbawa)
    candidate_indices = grid.get_candidate_indices(camera_pos, far_plane)
    assert len(candidate_indices) == 2  # Hanya 2 objek terdekat

    # 2. Precise Culling
    visible_indices = compute_distances_and_cull_grid(
        store, candidate_indices, camera_pos, near_plane=1.0, far_plane=far_plane
    )
    assert len(visible_indices) == 2