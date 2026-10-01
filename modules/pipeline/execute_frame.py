import numpy as np
from modules.vector_math import compute_distances_and_cull_grid
from modules.sorting.dod_sort import sort_opaque_fast, count_state_switches_dod


def execute_frame(pipeline, camera_pos: np.ndarray, near_plane: float = 1.0, far_plane: float = 200.0):
    """
    Menjalankan 1 frame lengkap pipeline:
    Spatial Query -> Vector Culling -> Bit-Packed Sorting -> State Switch Analysis
    """
    candidates = pipeline.grid.get_candidate_indices(camera_pos, far_plane)
    if len(candidates) == 0:
        pipeline.last_opaque_indices = np.array([], dtype=int)
        pipeline.last_state_switches = 0
        return pipeline.last_opaque_indices

    visible_indices = compute_distances_and_cull_grid(
        pipeline.store, candidates, camera_pos, near_plane, far_plane
    )

    pipeline.last_opaque_indices = sort_opaque_fast(pipeline.store, visible_indices)
    pipeline.last_state_switches = count_state_switches_dod(pipeline.store, pipeline.last_opaque_indices)

    return pipeline.last_opaque_indices