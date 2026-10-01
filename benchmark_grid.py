import time
import numpy as np
from modules.models.render_data import RenderDataStore
from modules.models.spatial_grid import SpatialGrid3D
from modules.vector_math import compute_distances_and_cull_grid


def run_grid_benchmark():
    count = 1_000_000
    print(f"==================================================")
    print(f"   SPATIAL GRID BENCHMARK ({count:,} OBJEK)")
    print(f"==================================================")

    store = RenderDataStore(capacity=count)
    # Sebar 1 juta objek di area sangat luas (-2000m s/d 2000m)
    positions = np.random.uniform(-2000, 2000, (count, 3)).astype(np.float32)
    mats = np.random.randint(1, 100, count, dtype=np.int32)
    trans = np.zeros(count, dtype=bool)

    store.add_objects(positions, mats, trans)

    # 1. Build Spatial Grid
    grid = SpatialGrid3D(cell_size=100.0)
    start_grid = time.perf_counter()
    grid.build_grid(store)
    grid_time = (time.perf_counter() - start_grid) * 1000
    print(f"Build Spatial Grid Time: {grid_time:.2f} ms")

    # 2. Query Real-Time Kamera
    camera_pos = np.array([0.0, 0.0, 0.0], dtype=np.float32)
    far_plane = 200.0

    start_query = time.perf_counter()
    candidates = grid.get_candidate_indices(camera_pos, far_plane)
    visible_indices = compute_distances_and_cull_grid(
        store, candidates, camera_pos, near_plane=1.0, far_plane=far_plane
    )
    query_time = (time.perf_counter() - start_query) * 1000

    print(f"Objek Kandidat Terperiksa : {len(candidates):,} / 1,000,000")
    print(f"Objek Lolos Culling       : {len(visible_indices):,}")
    print(f"Waktu Culling Per-Frame   : {query_time:.2f} ms")
    print(f"Estimasi Max FPS          : {1000 / query_time:.0f} FPS")
    print(f"==================================================")


if __name__ == "__main__":
    run_grid_benchmark()