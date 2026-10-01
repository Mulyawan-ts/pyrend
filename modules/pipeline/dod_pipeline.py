import numpy as np
from modules.models.render_data import RenderDataStore
from modules.models.spatial_grid import SpatialGrid3D
from modules.pipeline.load_scene import load_scene
from modules.pipeline.execute_frame import execute_frame


class DODRenderPipeline:
    def __init__(self, capacity: int = 1_000_000, cell_size: float = 100.0):
        self.store = RenderDataStore(capacity=capacity)
        self.grid = SpatialGrid3D(cell_size=cell_size)
        self.last_opaque_indices = np.array([], dtype=int)
        self.last_state_switches = 0

    def load_scene(self, positions: np.ndarray, material_ids: np.ndarray, is_transparent: np.ndarray):
        load_scene(self, positions, material_ids, is_transparent)

    def execute_frame(self, camera_pos: np.ndarray, near_plane: float = 1.0, far_plane: float = 200.0):
        return execute_frame(self, camera_pos, near_plane, far_plane)