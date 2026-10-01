def sort_front_to_back(objects):
    """
    Mengurutkan objek dari yang TERDEKAT ke TERJAUH (Kecil -> Besar).
    Cocok untuk objek padat (Opaque) agar menghemat overdraw.
    """
    return sorted(objects, key=lambda obj: obj.jarak)