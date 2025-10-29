import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

def preview_file(filepath):
    """
    Menampilkan isi file (gambar atau teks) dalam jendela baru.
    """
    win = tk.Toplevel()
    win.title(f"Pratinjau: {os.path.basename(filepath)}")
    win.geometry("600x500")

    ext = os.path.splitext(filepath)[1].lower()

    try:
        if ext in [".jpg", ".jpeg", ".png", ".gif"]:
            # Tampilkan gambar
            img = Image.open(filepath)
            img.thumbnail((580, 400))
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(win, image=photo)
            label.image = photo
            label.pack(pady=10)
        elif ext in [".txt"]:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            box = ScrolledText(win, wrap=tk.WORD)
            box.insert(tk.END, content)
            box.pack(expand=True, fill="both")
        elif ext in [".pdf"]:
            label = tk.Label(win, text="🔒 Pratinjau PDF belum didukung.")
            label.pack(pady=20)
        else:
            label = tk.Label(win, text="⚠️ Jenis file ini belum didukung untuk pratinjau.")
            label.pack(pady=20)
    except Exception as e:
        label = tk.Label(win, text=f"Gagal memuat file: {e}")
        label.pack(pady=20)
