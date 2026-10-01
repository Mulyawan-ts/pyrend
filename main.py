from modules.models.render_object import RenderObject
from modules.culling import CameraFrustum
from modules.pipeline import RenderPipeline


def main():
    # Objek dengan posisi 3D (X, Y, Z)
    scene = [
        RenderObject(nama="Pohon A", x=0.0, y=0.0, z=10.0, material_id=101),
        RenderObject(nama="Pagar B", x=5.0, y=0.0, z=2.0, material_id=101),
        RenderObject(nama="Awan C", x=0.0, y=20.0, z=50.0, material_id=200, transparan=True),
    ]

    # Kamera posisi awal di (0, 0, 0)
    camera = CameraFrustum(x=0.0, y=0.0, z=0.0, near_plane=1.0, far_plane=100.0)
    pipeline = RenderPipeline(camera=camera)

    print("--- FRAME 1: Kamera di (0, 0, 0) ---")
    pipeline.submit(scene)
    pipeline.process_and_render()

    print("\n--- FRAME 2: Kamera maju ke (0, 0, 8.0) ---")
    camera.z = 8.0  # Pindah kamera mendekati Pohon A
    pipeline.submit(scene)
    pipeline.process_and_render()


if __name__ == "__main__":
    main()