def sort_by_material_then_depth(objects):
    """
    Mengurutkan objek padat berdasarkan:
    1. material_id (Kecil -> Besar) agar mengganti material sejarang mungkin (State Batching)
    2. jarak (Terdekat -> Terjauh) untuk efisiensi Early-Z
    """
    return sorted(objects, key=lambda obj: (obj.material_id, obj.jarak))