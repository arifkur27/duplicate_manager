import customtkinter as ctk
import os
import platform
import subprocess
from tkinter import Toplevel, messagebox
from PIL import Image

# ======================================================
# UTILITY FUNCTIONS
# ======================================================

def get_file_size_human(size_bytes):
    """Mengubah ukuran byte menjadi format yang mudah dibaca (KB, MB, GB)."""
    if size_bytes < 1024:
        return f"{size_bytes} Bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def open_file_explorer(path):
    """Membuka folder lokasi file di File Explorer (Windows/Linux/macOS)."""
    if platform.system() == "Windows":
        subprocess.Popen(['explorer', '/select,', path])
    elif platform.system() == "Darwin": # macOS
        subprocess.Popen(['open', '-R', path])
    else: # Linux
        subprocess.Popen(['xdg-open', os.path.dirname(path)])

# ======================================================
# MAIN PREVIEW FUNCTION
# ======================================================

class PreviewWindow(ctk.CTkToplevel):
    def __init__(self, parent, file_path):
        super().__init__(parent)
        self.file_path = file_path
        self.parent = parent
        self.title("Preview File Duplikat")
        self.geometry("600x450")
        self.resizable(False, False)
        
        # Mencegah interaksi dengan window utama
        self.grab_set() 
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"File tidak ditemukan: {file_path}")
            self.destroy()
            return

        self.file_name = os.path.basename(file_path)
        self.file_dir = os.path.dirname(file_path)
        self.file_ext = os.path.splitext(self.file_name)[1].lower()
        self.file_size = os.path.getsize(file_path)

        self.build_ui()

    def build_ui(self):
        # Frame Judul dan Info
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        # Judul (Nama File)
        ctk.CTkLabel(
            info_frame,
            text=self.file_name,
            font=("Poppins", 16, "bold"),
            wraplength=550,
        ).pack(anchor="w")

        # Info Path dan Ukuran
        ctk.CTkLabel(
            info_frame,
            text=f"Path: {self.file_dir}",
            font=("Inter", 10),
            wraplength=550,
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=f"Ukuran: {get_file_size_human(self.file_size)}",
            font=("Inter", 10),
        ).pack(anchor="w")

        # Tombol Aksi
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(pady=10)
        
        ctk.CTkButton(
            action_frame, text="Buka Lokasi Folder", 
            command=lambda: open_file_explorer(self.file_path),
            fg_color="#3A0CA3"
        ).pack(side="left", padx=10)
        
        # Area Konten Preview
        content_frame = ctk.CTkFrame(self, fg_color=("white", "#2B2B40"))
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.show_content_preview(content_frame)

    def show_content_preview(self, container):
        """Menampilkan konten file (gambar atau teks) di container."""
        
        if self.file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico']:
            try:
                # Upaya menampilkan gambar
                img = Image.open(self.file_path)
                
                # Resize gambar agar pas di frame (Maksimal 300x300)
                max_size = (300, 300)
                img.thumbnail(max_size)
                
                # Konversi ke CTkImage dan tampilkan
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                
                ctk.CTkLabel(container, text="", image=ctk_img).pack(expand=True)
                
            except Exception as e:
                ctk.CTkLabel(container, text=f"⚠️ Gagal memuat gambar: {e}", text_color="red").pack(pady=50)

        elif self.file_ext in ['.txt', '.log', '.csv', '.py', '.html', '.css', '.js']:
            # Upaya menampilkan 10 baris pertama file teks
            try:
                with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    preview_text = f.read(1024) # Baca 1 KB pertama
                    
                textbox = ctk.CTkTextbox(container, wrap="word", width=500, height=300)
                textbox.insert("1.0", preview_text + "\n\n--- [Hanya menampilkan 1 KB pertama] ---")
                textbox.configure(state="disabled")
                textbox.pack(padx=10, pady=10, fill="both", expand=True)

            except Exception as e:
                ctk.CTkLabel(container, text=f"⚠️ Gagal membaca teks: {e}", text_color="red").pack(pady=50)
                
        else:
            # Format file tidak didukung
            ctk.CTkLabel(
                container, 
                text=f"Tidak ada preview tersedia untuk format '{self.file_ext}'.", 
                font=("Poppins", 14),
                text_color="#B3B3B3"
            ).pack(pady=50)

# ======================================================
# FUNCTION YANG DIPANGGIL DARI main_window.py
# ======================================================
def show_preview_window(parent, file_path):
    # Cek jika file_path valid
    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"File tidak ditemukan: {file_path}")
        return
        
    # Instansiasi kelas PreviewWindow
    PreviewWindow(parent, file_path)

# Pastikan Anda sudah menginstal Pillow: pip install Pillow