import numpy as np
import pytest
from modules.models.render_data import RenderDataStore
from modules.vector_math import compute_distances_and_cull
from modules.sorting.dod_sort import (
    sort_opaque_dod,
    sort_transparent_dod,
    count_state_switches_dod,
)


def test_dod_culling_and_sorting():
    store = RenderDataStore(capacity=10)

    # Buat 4 objek sampel
    positions = np.array([
        [0.0, 0.0, 10.0],  # Pohon A (mat 101, opaque)
        [0.0, 0.0, 2.0],   # Pagar (mat 101, opaque)
        [0.0, 0.0, 3.0],   # Tembok (mat 102, opaque)
        [0.0, 0.0, 3.0],   # Kaca (mat 200, transparent)
    ], dtype=np.float32)

    mats = np.array([101, 101, 102, 200], dtype=np.int32)
    trans = np.array([False, False, False, True], dtype=bool)

    store.add_objects(positions, mats, trans)
    camera_pos = np.array([0.0, 0.0, 0.0], dtype=np.float32)

    # 1. Culling
    visible_mask = compute_distances_and_cull(store, camera_pos, near_plane=1.0, far_plane=50.0)
    assert np.sum(visible_mask) == 4

    # 2. Sorting Opaque
    opaque_indices = sort_opaque_dod(store, visible_mask)
    assert len(opaque_indices) == 3
    # Harus terkelompok mat 101 dulu (index 1 & 0), baru mat 102 (index 2)
    assert store.material_ids[opaque_indices[0]] == 101
    assert store.material_ids[opaque_indices[1]] == 101
    assert store.material_ids[opaque_indices[2]] == 102

    # 3. State Switches
    switches = count_state_switches_dod(store, opaque_indices)
    assert switches == 2  # Material 101 -> Material 102