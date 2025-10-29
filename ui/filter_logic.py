import os

def filter_duplicates(duplicates, tipe):
    if tipe == "Semua":
        return duplicates

    def kategori(path):
        ext = os.path.splitext(path)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".gif"]:
            return "Foto"
        elif ext in [".txt", ".pdf", ".doc", ".docx"]:
            return "Dokumen"
        else:
            return "Lainnya"

    return [
        (f1, f2) for f1, f2 in duplicates
        if kategori(f1) == tipe or kategori(f2) == tipe
    ]
