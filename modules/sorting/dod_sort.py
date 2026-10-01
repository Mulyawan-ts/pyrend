import numpy as np


def sort_opaque_fast(store, visible_mask: np.ndarray) -> np.ndarray:
    """Bit-Packed Fast Sorting untuk objek Opaque."""
    if not np.any(visible_mask):
        return np.array([], dtype=int)

    # Filter hanya objek visible & opaque
    opaque_mask = visible_mask & (~store.is_transparent[: store.count])
    indices = np.where(opaque_mask)[0]

    if len(indices) == 0:
        return np.array([], dtype=int)

    # Gabungkan Material ID (MSB 32-bit) dan Distance (LSB 32-bit) menjadi UInt64
    mats = store.material_ids[indices].astype(np.uint64) << 32
    dists = store.distances[indices].view(np.uint32).astype(np.uint64)

    packed_keys = mats | dists
    sorted_order = np.argsort(packed_keys)

    return indices[sorted_order]


def sort_opaque_dod(store, visible_mask: np.ndarray) -> np.ndarray:
    if not np.any(visible_mask):
        return np.array([], dtype=int)

    opaque_mask = visible_mask & (~store.is_transparent[: store.count])
    indices = np.where(opaque_mask)[0]

    if len(indices) == 0:
        return np.array([], dtype=int)

    keys = (store.distances[indices], store.material_ids[indices])
    sorted_order = np.lexsort(keys)

    return indices[sorted_order]


def sort_transparent_dod(store, visible_mask: np.ndarray) -> np.ndarray:
    if not np.any(visible_mask):
        return np.array([], dtype=int)

    trans_mask = visible_mask & store.is_transparent[: store.count]
    indices = np.where(trans_mask)[0]

    if len(indices) == 0:
        return np.array([], dtype=int)

    sorted_order = np.argsort(-store.distances[indices])

    return indices[sorted_order]


def count_state_switches_dod(store, sorted_indices: np.ndarray) -> int:
    if len(sorted_indices) == 0:
        return 0

    materials = store.material_ids[sorted_indices]
    switches = np.count_nonzero(materials[1:] != materials[:-1])

    return switches + 1