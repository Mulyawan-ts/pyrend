import pytest
from modules.models.render_object import RenderObject
from modules.sorting.front_to_back import sort_front_to_back
from modules.sorting.back_to_front import sort_back_to_front


@pytest.fixture
def sample_objects():
    return [
        RenderObject(nama="Pohon", jarak=10.0),
        RenderObject(nama="Kaca", jarak=3.0, transparan=True),
        RenderObject(nama="Awan", jarak=50.0, transparan=True),
        RenderObject(nama="Rumah", jarak=10.0),
    ]


def test_front_to_back_normal(sample_objects):
    hasil = sort_front_to_back(sample_objects)
    jarak = [obj.jarak for obj in hasil]
    assert jarak == [3.0, 10.0, 10.0, 50.0]


def test_front_to_back_empty():
    assert sort_front_to_back([]) == []


def test_back_to_front_normal(sample_objects):
    hasil = sort_back_to_front(sample_objects)
    jarak = [obj.jarak for obj in hasil]
    assert jarak == [50.0, 10.0, 10.0, 3.0]


def test_back_to_front_empty():
    assert sort_back_to_front([]) == []