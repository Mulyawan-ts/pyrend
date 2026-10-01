import numpy as np


class RenderDataStore:
    def __init__(self, capacity: int = 1_000_000):
        self.capacity = capacity
        self.count = 0

        # Alokasi memori kontigu langsung di awal (sekitar 16 MB total)
        self.positions = np.zeros((capacity, 3), dtype=np.float32)
        self.material_ids = np.zeros(capacity, dtype=np.int32)
        self.is_transparent = np.zeros(capacity, dtype=bool)
        self.distances = np.zeros(capacity, dtype=np.float32)

    def add_objects(self, positions: np.ndarray, material_ids: np.ndarray, is_transparent: np.ndarray):
        n = len(positions)
        if self.count + n > self.capacity:
            raise MemoryError(f"Kapasitas DataStore ({self.capacity:,}) terlampaui!")

        idx_start = self.count
        idx_end = self.count + n

        self.positions[idx_start:idx_end] = positions
        self.material_ids[idx_start:idx_end] = material_ids
        self.is_transparent[idx_start:idx_end] = is_transparent

        self.count += n

    def clear(self):
        self.count = 0