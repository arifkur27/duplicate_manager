import os
import csv
import time
from concurrent.futures import ThreadPoolExecutor
from .file_hash import quick_hash, full_hash
from core.utils import resource_path   # ✅ penting untuk exe

# ✅ path aman untuk python & exe
LOG_PATH = resource_path("data/duplikat_log.csv")

def scan_folder(folder_path, progress_callback=None, finish_callback=None):
    start_time = time.time()
    hash_map = {}
    duplicates = []

    all_files = []
    for root, _, files in os.walk(folder_path):
        for name in files:
            all_files.append(os.path.join(root, name))

    total_files = len(all_files)
    scanned = 0

    for path in all_files:
        scanned += 1

        if progress_callback:
            progress_callback(path, scanned, total_files)

        q_hash = quick_hash(path)
        if not q_hash:
            continue

        if q_hash in hash_map:
            f1, f2 = hash_map[q_hash], path
            if full_hash(f1) == full_hash(f2):
                duplicates.append((f1, f2))
        else:
            hash_map[q_hash] = path

    # ✅ buat folder data jika belum ada
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    # ✅ simpan log
    if duplicates:
        with open(LOG_PATH, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["File 1", "File 2"])
            writer.writerows(duplicates)

    # ✅ kirim info selesai
    total_time = round(time.time() - start_time, 2)
    if finish_callback:
        finish_callback(total_files, len(duplicates), total_time)

    return duplicates
