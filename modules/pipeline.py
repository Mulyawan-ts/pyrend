from modules.culling import CameraFrustum, cull_objects
from modules.sorting.material_sort import sort_by_material_then_depth
from modules.sorting.back_to_front import sort_back_to_front
from modules.stats import RenderStats


class RenderPipeline:
    def __init__(self, camera=None):
        self.camera = camera or CameraFrustum()
        self.opaque_objects = []
        self.transparent_objects = []
        self.stats = RenderStats()

    def submit(self, render_objects):
        # 1. Frustum Culling: Hilangkan objek di luar jangkauan pandang kamera
        visible_objects = cull_objects(render_objects, self.camera)

        # 2. Pisahkan objek terlihat berdasarkan tipe
        self.opaque_objects = [obj for obj in visible_objects if not obj.transparan]
        self.transparent_objects = [obj for obj in visible_objects if obj.transparan]

    def process_and_render(self):
        self.stats.reset()
        self.stats.total_objects = len(self.opaque_objects) + len(self.transparent_objects)

        # 3. Sorting Objek Terlihat
        sorted_opaque = sort_by_material_then_depth(self.opaque_objects)
        sorted_transparent = sort_back_to_front(self.transparent_objects)

        current_mat = None

        print("=== RENDERING OPAQUE PASS ===")
        for obj in sorted_opaque:
            if obj.material_id != current_mat:
                current_mat = obj.material_id
                self.stats.record_switch()
                print(f"  [Switch Material -> ID: {current_mat}]")
            
            self.stats.record_draw()
            print(f"    [Draw Opaque] {obj.nama} (Jarak: {obj.jarak}m)")

        print("\n=== RENDERING TRANSPARENT PASS ===")
        for obj in sorted_transparent:
            if obj.material_id != current_mat:
                current_mat = obj.material_id
                self.stats.record_switch()
                print(f"  [Switch Material -> ID: {current_mat}]")

            self.stats.record_draw()
            print(f"    [Draw Transparent] {obj.nama} (Jarak: {obj.jarak}m)")

        self.stats.print_summary()