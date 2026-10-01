from dataclasses import dataclass

@dataclass
class RenderStats:
    draw_call_count: int = 0
    state_switch_count: int = 0
    total_objects: int = 0

    def reset(self):
        """Reset statistik sebelum frame baru digambar."""
        self.draw_call_count = 0
        self.state_switch_count = 0
        self.total_objects = 0

    def record_draw(self):
        self.draw_call_count += 1

    def record_switch(self):
        self.state_switch_count += 1

    def print_summary(self):
        print("\n" + "=" * 35)
        print("      RENDER ENGINE STATS      ")
        print("=" * 35)
        print(f" Total Objek   : {self.total_objects}")
        print(f" Draw Calls    : {self.draw_call_count}")
        print(f" State Switches: {self.state_switch_count}")
        print("=" * 35)