import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import os

def show_preview_window(master, filepath):
    win = tk.Toplevel(master)
    win.title(f"Pratinjau: {os.path.basename(filepath)}")
    win.geometry("700x600")

    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext in [".jpg", ".jpeg", ".png", ".gif"]:
            img = Image.open(filepath)
            img.thumbnail((680, 480))
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
        else:
            tk.Label(win, text="⚠️ Pratinjau jenis file ini belum didukung.").pack(pady=20)
    except Exception as e:
        tk.Label(win, text=f"Gagal membuka file: {e}").pack(pady=20)
