import numpy as np


def load_scene(pipeline, positions: np.ndarray, material_ids: np.ndarray, is_transparent: np.ndarray):
    """Memuat seluruh data objek ke DataStore dan membangun Spatial Grid."""
    pipeline.store.clear()
    pipeline.store.add_objects(positions, material_ids, is_transparent)
    pipeline.grid.build_grid(pipeline.store)