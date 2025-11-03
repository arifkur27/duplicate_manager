import customtkinter as ctk
from tkinter import messagebox, filedialog
from core.file_scan import scan_folder
from core.file_delete import delete_file
from ui.preview_window import show_preview_window
from ui.filter_logic import filter_duplicates
import time


class DuplicateManagerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Duplicate File Manager")
        self.geometry("1000x600")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # State
        self.folder_path = ctk.StringVar()
        self.duplicates = []
        self.filtered_duplicates = []
        self.start_time = None
        self.checkbox_vars = []  # untuk checkbox

        self.build_ui()

    # ======================================================
    #                       UI SETUP
    # ======================================================
    def build_ui(self):
        self.build_header()
        self.build_folder_bar()
        self.build_filter_section()
        self.build_list_area()
        self.build_progress_info()
        self.build_footer_buttons()
        self.build_footer()

    def build_header(self):
        header = ctk.CTkFrame(self, height=50, fg_color="#2D6A4F")
        header.pack(fill="x")
        ctk.CTkLabel(
            header, text="Duplicate File Manager",
            font=("Segoe UI", 18, "bold"), text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

    def build_folder_bar(self):
        bar = ctk.CTkFrame(self)
        bar.pack(fill="x", pady=(5, 5))

        ctk.CTkButton(
            bar, text="📁 Pilih Folder", width=130,
            fg_color="#74C69D", text_color="black",
            command=self.select_folder
        ).pack(side="left", padx=5)

        ctk.CTkEntry(
            bar, textvariable=self.folder_path, width=600
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bar, text="🔎 Cari Duplikat", width=130,
            fg_color="#40916C", text_color="white",
            command=self.find_duplicates
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bar, text="🔄 Refresh", width=100,
            fg_color="#1D9BF0", text_color="white",
            command=self.refresh_view
        ).pack(side="left", padx=5)

    def build_filter_section(self):
        section = ctk.CTkFrame(self)
        section.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(section, text="Filter jenis file:").pack(side="left", padx=5)

        self.filter_var = ctk.StringVar(value="Semua")
        self.filter_box = ctk.CTkComboBox(
            section, variable=self.filter_var, width=180,
            values=["Semua", "Foto", "Dokumen", "Lainnya"]
        )
        self.filter_box.pack(side="left", padx=5)

        ctk.CTkButton(
            section, text="Terapkan Filter", width=120,
            fg_color="#74C69D", text_color="black",
            command=self.apply_filter
        ).pack(side="left", padx=5)

    def build_list_area(self):
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=(0, 5))
        self.scroll = ctk.CTkScrollableFrame(container, width=900)
        self.scroll.pack(fill="both", expand=True)
        self.checkbox_vars = []

    def build_progress_info(self):
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=(5, 2))
        self.progress.set(0)

        self.info_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 11))
        self.info_label.pack(pady=(0, 5))

    def build_footer_buttons(self):
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(pady=10)

        ctk.CTkButton(
            bottom, text="✅ Pilih Semua", width=150,
            fg_color="#1B9C85", text_color="white",
            font=("Segoe UI", 14, "bold"), corner_radius=10,
            command=self.select_all
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            bottom, text="❌ Hapus Centang", width=150,
            fg_color="#6c757d", text_color="white",
            font=("Segoe UI", 14, "bold"), corner_radius=10,
            command=self.clear_all
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            bottom, text="🗑️ Hapus File Terpilih", width=200,
            fg_color="#D00000", text_color="white",
            font=("Segoe UI", 14, "bold"), corner_radius=10,
            command=self.remove_selected
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            bottom, text="⚠️ Hapus Semua Duplikat", width=200,
            fg_color="#FFB703", text_color="black",
            font=("Segoe UI", 14, "bold"), corner_radius=10,
            command=self.remove_all_duplicates
        ).pack(side="left", padx=10)

    def build_footer(self):
        footer = ctk.CTkFrame(self, height=35, fg_color="#2D6A4F")
        footer.pack(fill="x", side="bottom")
        ctk.CTkLabel(
            footer, text="© 2025 Duplicate File Manager by Arif",
            text_color="white", font=("Segoe UI", 10)
        ).pack(pady=5)

    # ======================================================
    #                      FUNGSI
    # ======================================================

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def find_duplicates(self):
        if not self.folder_path.get():
            messagebox.showwarning("Peringatan", "Pilih folder terlebih dahulu!")
            return

        self.progress.set(0)
        self.info_label.configure(text="Mengumpulkan daftar file...")
        self.update_idletasks()

        self.start_time = time.time()
        self.duplicates = scan_folder(
            self.folder_path.get(),
            progress_callback=self.update_scan_progress,
            finish_callback=self.scan_finished
        )
        self.filtered_duplicates = self.duplicates
        self.show_duplicates_in_list(self.filtered_duplicates)

    def show_duplicates_in_list(self, data):
        for widget in self.scroll.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()

        for f1, f2 in data:
            row_frame = ctk.CTkFrame(self.scroll)
            row_frame.pack(fill="x", pady=2, padx=2)

            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(row_frame, text=f"{f1}   ⇄   {f2}", variable=var)
            cb.pack(side="left", fill="x", expand=True, padx=(5, 0))

            preview_btn = ctk.CTkButton(
                row_frame, text="👁️", width=40,
                fg_color="#40916C", text_color="white",
                command=lambda path=f2: show_preview_window(self, path)
            )
            preview_btn.pack(side="right", padx=5)

            self.checkbox_vars.append((var, f2))

    def update_scan_progress(self, path, scanned, total):
        percent = scanned / total
        self.progress.set(percent)

        elapsed = time.time() - self.start_time
        remaining = (elapsed / scanned * total - elapsed) if scanned > 0 else 0
        mins = int(remaining // 60)
        secs = int(remaining % 60)
        estimate_text = f"{mins}m {secs}s lagi" if remaining > 3 else "Sebentar lagi"

        self.info_label.configure(text=f"⏳ {scanned}/{total} file • Estimasi {estimate_text}")
        self.update_idletasks()

    def scan_finished(self, total_files, dup_count, seconds):
        self.info_label.configure(
            text=f"Scan selesai • {total_files} file • {dup_count} duplikat • {seconds} detik"
        )
        messagebox.showinfo(
            "Selesai",
            f"Scan selesai!\n\nTotal file: {total_files}\nDuplikat ditemukan: {dup_count}\nWaktu: {seconds} detik"
        )

    def apply_filter(self):
        if not self.duplicates:
            messagebox.showwarning("Tidak ada data", "Scan dahulu sebelum filter.")
            return

        tipe = self.filter_var.get()
        self.filtered_duplicates = filter_duplicates(self.duplicates, tipe)
        self.show_duplicates_in_list(self.filtered_duplicates)
        self.info_label.configure(
            text=f"Filter: {tipe} • {len(self.filtered_duplicates)} ditemukan"
        )

    def refresh_view(self):
        self.apply_filter()

    def select_all(self):
        for var, _ in self.checkbox_vars:
            var.set(True)

    def clear_all(self):
        for var, _ in self.checkbox_vars:
            var.set(False)

    def remove_selected(self):
        selected = [f for var, f in self.checkbox_vars if var.get()]
        if not selected:
            messagebox.showwarning("Tidak ada pilihan", "Centang file yang ingin dihapus.")
            return
        if messagebox.askyesno("Konfirmasi", f"Hapus {len(selected)} file terpilih?"):
            delete_file(selected)
            self.find_duplicates()

    def remove_all_duplicates(self):
        if not self.duplicates:
            messagebox.showwarning("Tidak ada duplikat", "Belum scan.")
            return
        if messagebox.askyesno("Konfirmasi", f"Hapus semua ({len(self.duplicates)}) duplikat?"):
            files = [f2 for f1, f2 in self.duplicates]
            delete_file(files)
            self.find_duplicates()
