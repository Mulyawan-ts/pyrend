def sort_back_to_front(objects):
    """
    Mengurutkan objek dari yang TERJAUH ke TERDEKAT (Besar -> Kecil).
    Cocok untuk objek transparan (glass, air) agar blending benar.
    """
    return sorted(objects, key=lambda obj: obj.jarak, reverse=True)