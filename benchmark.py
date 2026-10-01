import random
import time
import numpy as np
from modules.models.render_object import RenderObject
from modules.vector_math import calculate_distances_numpy


def run_numpy_benchmark(count: int = 100_000):
    print(f"==================================================")
    print(f"   BENCHMARK NUMPY DISTANCE ({count:,} OBJEK)")
    print(f"==================================================")

    # Generate 100,000 objek
    objects = [
        RenderObject(
            nama=f"Obj_{i}",
            x=random.uniform(-100, 100),
            y=random.uniform(-100, 100),
            z=random.uniform(0, 500),
        )
        for i in range(count)
    ]

    # 1. Native Python Loop
    start_py = time.perf_counter()
    for obj in objects:
        obj.update_distance(0.0, 0.0, 0.0)
    time_py = (time.perf_counter() - start_py) * 1000

    # 2. NumPy Vectorized
    start_np = time.perf_counter()
    calculate_distances_numpy(objects, 0.0, 0.0, 0.0)
    time_np = (time.perf_counter() - start_np) * 1000

    print(f"1. Native Python Loop : {time_py:.2f} ms")
    print(f"2. NumPy Vectorization: {time_np:.2f} ms")
    print(f"-> Speedup            : {time_py / time_np:.1f}x lebih cepat!")


if __name__ == "__main__":
    run_numpy_benchmark(100_000)