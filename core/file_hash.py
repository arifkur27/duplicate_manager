import hashlib

def quick_hash(path, chunk_size=4096):
    """Hash cepat (sebagian isi file)."""
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read(chunk_size)).hexdigest()
    except:
        return None

def full_hash(path, chunk_size=8192):
    """Hash penuh (seluruh isi file)."""
    try:
        h = hashlib.md5()
        with open(path, 'rb') as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
        return h.hexdigest()
    except:
        return None
