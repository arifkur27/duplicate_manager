import os
from tqdm import tqdm

def delete_file(file_paths):
    """
    Menghapus file duplikat dari sistem (benar-benar terhapus).
    """
    # Jika hanya 1 file (string), ubah ke list
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    for path in tqdm(file_paths, desc="Menghapus file", unit="file"):
        try:
            abs_path = os.path.abspath(path)  # pastikan path absolut
            if os.path.exists(abs_path):
                os.remove(abs_path)
                print(f"✅ Dihapus: {abs_path}")
            else:
                print(f"⚠️ File tidak ditemukan: {abs_path}")
        except PermissionError:
            print(f"❌ Tidak ada izin untuk menghapus: {abs_path}")
        except Exception as e:
            print(f"❌ Gagal menghapus {abs_path}: {e}")
