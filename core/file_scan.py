import os
import csv
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from .file_hash import quick_hash, full_hash

LOG_PATH = "data/duplikat_log.csv"

def scan_folder(folder_path):
    """Mencari file duplikat di folder."""
    hash_map = {}
    duplicates = []

    all_files = []
    for root, _, files in os.walk(folder_path):
        for name in files:
            path = os.path.join(root, name)
            all_files.append(path)

    with ThreadPoolExecutor() as executor:
        for path in tqdm(all_files, desc="Memindai file..."):
            q_hash = quick_hash(path)
            if not q_hash:
                continue

            if q_hash in hash_map:
                f1, f2 = hash_map[q_hash], path
                if full_hash(f1) == full_hash(f2):
                    duplicates.append((f1, f2))
            else:
                hash_map[q_hash] = path

    if duplicates:
        with open(LOG_PATH, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["File 1", "File 2"])
            writer.writerows(duplicates)

    return duplicates
