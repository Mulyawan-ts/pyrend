import pytest
from modules.models.render_object import RenderObject
from modules.pipeline import RenderPipeline


@pytest.fixture
def sample_scene():
    return [
        RenderObject(nama="Pohon A", jarak=10.0, material_id=101, transparan=False),
        RenderObject(nama="Pagar", jarak=2.0, material_id=101, transparan=False),
        RenderObject(nama="Tembok", jarak=3.0, material_id=102, transparan=False),
        RenderObject(nama="Kaca Jendela", jarak=3.0, material_id=200, transparan=True),
    ]


def test_pipeline_execution_and_stats(sample_scene):
    pipeline = RenderPipeline()
    pipeline.submit(sample_scene)
    pipeline.process_and_render()

    # Verifikasi data statistik render
    assert pipeline.stats.total_objects == 4
    assert pipeline.stats.draw_call_count == 4
    # Memastikan perpindahan material dihitung tepat (Material 101 -> 102 -> 200 = 3 switch)
    assert pipeline.stats.state_switch_count == 3