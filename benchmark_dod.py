import time
import numpy as np
from modules.models.render_data import RenderDataStore
from modules.vector_math import compute_distances_and_cull
from modules.sorting.dod_sort import (
    sort_opaque_dod,
    sort_transparent_dod,
    count_state_switches_dod,
)


def run_1M_benchmark():
    count = 1_000_000
    print("==================================================")
    print(f"   BENCHMARK DATA-ORIENTED DESIGN ({count:,} OBJEK)")
    print("==================================================")

    print("Membuat 1 Juta Objek di memori...")
    start_gen = time.perf_counter()
    store = RenderDataStore(capacity=count)

    positions = np.random.uniform(-500, 500, (count, 3)).astype(np.float32)
    mats = np.random.randint(1, 200, count, dtype=np.int32)
    trans = np.random.choice([True, False], count, p=[0.1, 0.9])

    store.add_objects(positions, mats, trans)
    gen_time = time.perf_counter() - start_gen
    print(f"-> Selesai alokasi 1 Juta objek dalam {gen_time:.2f} detik.\n")

    camera_pos = np.array([0.0, 0.0, 0.0], dtype=np.float32)

    # --- SIMULASI PIPELINE REAL-TIME ---
    start_pipeline = time.perf_counter()

    # 1. Distance & Culling (100% Vectorized C)
    visible_mask = compute_distances_and_cull(
        store, camera_pos, near_plane=1.0, far_plane=250.0
    )

    # 2. Sorting Opaque & Transparent
    opaque_indices = sort_opaque_dod(store, visible_mask)
    trans_indices = sort_transparent_dod(store, visible_mask)

    # 3. State Switches Calculation
    switches = count_state_switches_dod(store, opaque_indices)

    total_time_ms = (time.perf_counter() - start_pipeline) * 1000

    print("--- HASIL EKSEKUSI PIPELINE ---")
    print(f"Total Objek di Scene : {count:,}")
    print(f"Objek Lolos Culling  : {np.sum(visible_mask):,}")
    print(f"Opaque Processed     : {len(opaque_indices):,}")
    print(f"Transparent Processed: {len(trans_indices):,}")
    print(f"State Switches       : {switches:,}")
    print(f"--------------------------------------------------")
    print(f" PIPELINE TIME       : {total_time_ms:.2f} ms")
    print(f" ESTIMASI FPS MAX    : {1000 / total_time_ms:.1f} FPS")
    print("==================================================")


if __name__ == "__main__":
    run_1M_benchmark()