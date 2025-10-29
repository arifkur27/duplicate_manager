import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from core.file_scan import scan_folder
from core.file_delete import delete_file
from ui.preview_window import show_preview_window
from ui.filter_logic import filter_duplicates


class DuplicateManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("🔍 Duplicate File Manager")
        master.geometry("820x550")
        master.config(bg="#f0f4f7")

        self.folder_path = ""
        self.duplicates = []
        self.filtered_duplicates = []

        # Header
        tk.Label(master, text="Duplicate File Manager",
                 font=("Segoe UI", 18, "bold"),
                 bg="#2D6A4F", fg="white", pady=10).pack(fill=tk.X)

        # Main Frame
        main_frame = tk.Frame(master, bg="#f0f4f7", padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Pilih folder untuk mencari file duplikat:",
                 font=("Segoe UI", 11), bg="#f0f4f7").pack(anchor="w", pady=(5, 2))

        # Tombol Pilih & Cari
        btn_frame = tk.Frame(main_frame, bg="#f0f4f7")
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Button(btn_frame, text="📁 Pilih Folder",
                  bg="#95D5B2", fg="black",
                  font=("Segoe UI", 10, "bold"),
                  command=self.select_folder,
                  relief="flat", width=15).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(btn_frame, text="🔎 Cari Duplikat",
                  bg="#52B788", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  command=self.find_duplicates,
                  relief="flat", width=15).pack(side=tk.LEFT)

        # Filter
        filter_frame = tk.Frame(main_frame, bg="#f0f4f7")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(filter_frame, text="Filter jenis file:", bg="#f0f4f7",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.filter_var = tk.StringVar()
        self.filter_box = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                       state="readonly",
                                       values=["Semua", "Foto", "Dokumen", "Lainnya"])
        self.filter_box.current(0)
        self.filter_box.pack(side=tk.LEFT, padx=10)
        tk.Button(filter_frame, text="Terapkan Filter",
                  command=self.apply_filter,
                  bg="#74C69D", font=("Segoe UI", 9, "bold"),
                  relief="flat").pack(side=tk.LEFT)

        # Listbox
        list_frame = tk.Frame(main_frame, bg="#f0f4f7")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(list_frame, width=100, height=15,
                                  yscrollcommand=self.scrollbar.set,
                                  font=("Consolas", 10), bg="#ffffff",
                                  fg="#333333", selectbackground="#74C69D",
                                  relief="flat")
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        # Tombol aksi
        button_frame = tk.Frame(main_frame, bg="#f0f4f7")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="👁️ Lihat File Terpilih",
                  bg="#118AB2", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  command=self.preview_selected,
                  relief="flat", width=20).pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="🗑️ Hapus File Terpilih",
                  bg="#D00000", fg="white",
                  font=("Segoe UI", 10, "bold"),
                  command=self.remove_selected,
                  relief="flat", width=20).pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="⚠️ Hapus Semua Duplikat",
                  bg="#FFB703", fg="black",
                  font=("Segoe UI", 10, "bold"),
                  command=self.remove_all_duplicates,
                  relief="flat", width=20).pack(side=tk.LEFT, padx=10)

        # Footer
        tk.Label(master, text="© 2025 Duplicate File Manager by Arif",
                 bg="#2D6A4F", fg="white",
                 font=("Segoe UI", 9), pady=5).pack(fill=tk.X, side=tk.BOTTOM)

    # --- Fungsi ---
    def select_folder(self):
        from tkinter import filedialog
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            messagebox.showinfo("Folder Dipilih", f"Folder: {self.folder_path}")

    def find_duplicates(self):
        if not self.folder_path:
            messagebox.showwarning("Peringatan", "Pilih folder terlebih dahulu!")
            return
        self.listbox.delete(0, tk.END)
        self.duplicates = scan_folder(self.folder_path)
        self.filtered_duplicates = self.duplicates
        if self.duplicates:
            for f1, f2 in self.duplicates:
                self.listbox.insert(tk.END, f"{f1} ⇄ {f2}")
            messagebox.showinfo("Selesai", f"Ditemukan {len(self.duplicates)} duplikat.")
        else:
            messagebox.showinfo("Hasil", "Tidak ada duplikat ditemukan.")

    def apply_filter(self):
        if not self.duplicates:
            messagebox.showwarning("Tidak ada data", "Lakukan pencarian duplikat terlebih dahulu.")
            return
        tipe = self.filter_var.get()
        self.filtered_duplicates = filter_duplicates(self.duplicates, tipe)
        self.listbox.delete(0, tk.END)
        for f1, f2 in self.filtered_duplicates:
            self.listbox.insert(tk.END, f"{f1} ⇄ {f2}")

    def preview_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih file untuk dilihat.")
            return
        selected = self.listbox.get(selection[0])
        file_to_preview = selected.split("⇄")[-1].strip()
        show_preview_window(self.master, file_to_preview)

    def remove_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Peringatan", "Pilih file duplikat yang ingin dihapus.")
            return
        selected = self.listbox.get(selection[0])
        file_to_delete = selected.split("⇄")[-1].strip()
        confirm = messagebox.askyesno("Konfirmasi", f"Hapus file ini dari sistem?\n\n{file_to_delete}")
        if confirm:
            delete_file([file_to_delete])
            self.listbox.delete(selection[0])
            messagebox.showinfo("Berhasil", f"File dihapus:\n{file_to_delete}")

    def remove_all_duplicates(self):
        if not self.duplicates:
            messagebox.showwarning("Tidak ada duplikat", "Belum ada hasil scan duplikat.")
            return
        confirm = messagebox.askyesno(
            "Konfirmasi",
            f"Akan menghapus {len(self.duplicates)} file duplikat dari komputer.\nLanjutkan?")
        if not confirm:
            return
        all_files_to_delete = [f2 for _, f2 in self.duplicates]
        delete_file(all_files_to_delete)
        self.listbox.delete(0, tk.END)
        self.duplicates = []
        messagebox.showinfo("Selesai", "Semua file duplikat berhasil dihapus permanen!")
