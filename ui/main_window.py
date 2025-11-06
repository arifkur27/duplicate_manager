import customtkinter as ctk
from tkinter import messagebox, filedialog
from core.file_scan import scan_folder
from core.file_delete import delete_file
from ui.preview_window import show_preview_window
from ui.filter_logic import filter_duplicates
from ui.about import AboutFrame
import time


class DuplicateManagerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Duplicate File Manager")
        self.geometry("1000x600")

        # Tema default (Light/Dark)
        self.current_theme = ctk.get_appearance_mode()
        ctk.set_default_color_theme("blue")

        # Warna elegan & soft
        self.primary_color = "#5A5BF3"      # biru lembut
        self.secondary_color = "#E9ECEF"    # abu muda
        self.header_color = "#2C2C54"       # biru tua keungu
        self.button_hover = "#6C63FF"       # warna hover lembut
        self.delete_color = "#E63946"       # merah lembut

        # State
        self.folder_path = ctk.StringVar()
        self.duplicates = []
        self.filtered_duplicates = []
        self.start_time = None
        self.checkbox_vars = []
        self.showing_about = False

        # Bangun UI
        self.build_ui()

    # ======================================================
    #                       UI SETUP
    # ======================================================
    def build_ui(self):
        self.build_header()
        self.build_folder_bar()
        self.build_filter_section()

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_progress_info()
        self.build_footer_buttons()
        self.build_footer()

        self.show_home_page()

    # ======================================================
    #                       HEADER
    # ======================================================
    def build_header(self):
        header = ctk.CTkFrame(self, height=55, fg_color=self.header_color)
        header.pack(fill="x", pady=(0, 3))

        ctk.CTkLabel(
            header,
            text="Duplicate File Manager",
            font=("Poppins", 20, "bold"),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkButton(
            header, text="ℹ️", width=40, height=32,
            corner_radius=8, fg_color=self.primary_color,
            hover_color=self.button_hover, text_color="white",
            command=self.toggle_about_page
        ).pack(side="right", padx=10, pady=5)

        self.theme_button = ctk.CTkSegmentedButton(
            header, values=["Light", "Dark"], command=self.change_theme
        )
        self.theme_button.pack(side="right", padx=10, pady=5)
        self.theme_button.set(self.current_theme)

    # ======================================================
    #                       BAR FOLDER
    # ======================================================
    def build_folder_bar(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", pady=(5, 5))

        ctk.CTkButton(
            bar, text="📁 Pilih Folder", width=130,
            fg_color=self.primary_color, text_color="white",
            hover_color=self.button_hover,
            command=self.select_folder
        ).pack(side="left", padx=5)

        ctk.CTkEntry(bar, textvariable=self.folder_path, width=550).pack(side="left", padx=5)

        ctk.CTkButton(
            bar, text="🔍 Cari Duplikat", width=130,
            fg_color="#3A0CA3", text_color="white",
            hover_color="#5F0F40",
            command=self.find_duplicates
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bar, text="↻", width=50,
            fg_color="#B3B3B3", text_color="black",
            hover_color="#A0A0A0",
            command=self.refresh_view
        ).pack(side="left", padx=5)

    # ======================================================
    #                       FILTER
    # ======================================================
    def build_filter_section(self):
        section = ctk.CTkFrame(self, fg_color="transparent")
        section.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(section, text="Filter jenis file:", font=("Poppins", 12, "bold")).pack(side="left", padx=5)

        self.filter_var = ctk.StringVar(value="Semua")
        self.filter_box = ctk.CTkComboBox(
            section, variable=self.filter_var, width=180,
            values=["Semua", "Foto", "Dokumen", "Lainnya"]
        )
        self.filter_box.pack(side="left", padx=5)

        ctk.CTkButton(
            section, text="Terapkan Filter", width=120,
            fg_color=self.primary_color, text_color="white",
            hover_color=self.button_hover,
            command=self.apply_filter
        ).pack(side="left", padx=5)

    # ======================================================
    #                       PROGRESS
    # ======================================================
    def build_progress_info(self):
        self.progress = ctk.CTkProgressBar(self, width=400, progress_color=self.primary_color)
        self.progress.pack(pady=(5, 2))
        self.progress.set(0)

        self.info_label = ctk.CTkLabel(self, text="", font=("Poppins", 11))
        self.info_label.pack(pady=(0, 5))

    # ======================================================
    #                       FOOTER BUTTONS
    # ======================================================
    def build_footer_buttons(self):
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.pack(pady=10)

        buttons = [
            ("Pilih Semua", self.primary_color, self.select_all),
            ("Hapus Centang", "#6C757D", self.clear_all),
            ("Hapus Terpilih", self.delete_color, self.remove_selected),
            ("Hapus Semua", "#E59819", self.remove_all_duplicates),
        ]

        for text, color, cmd in buttons:
            ctk.CTkButton(
                bottom, text=text, width=180,
                fg_color=color, text_color="white",
                font=("Poppins", 13, "bold"),
                corner_radius=10, command=cmd
            ).pack(side="left", padx=10)

    def build_footer(self):
        footer = ctk.CTkFrame(self, height=35, fg_color=self.header_color)
        footer.pack(fill="x", side="bottom")
        ctk.CTkLabel(
            footer, text="© 2025 Duplicate File Manager by Nasywa",
            text_color="white", font=("Poppins", 10)
        ).pack(pady=5)

    # ======================================================
    #                   HALAMAN & FUNGSI
    # ======================================================
    def show_home_page(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.scroll = ctk.CTkScrollableFrame(self.main_frame, width=900)
        self.scroll.pack(fill="both", expand=True)
        self.checkbox_vars = []

    def toggle_about_page(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        if not self.showing_about:
            AboutFrame(self.main_frame).pack(fill="both", expand=True)
            self.showing_about = True
        else:
            self.show_home_page()
            self.showing_about = False

    # ======================================================
    #                   LOGIKA UTAMA
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
        self.info_label.configure(text="🔎 Mengumpulkan daftar file...")
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
        self.show_home_page()
        for f1, f2 in data:
            row_frame = ctk.CTkFrame(
                self.scroll,
                fg_color="#E9F5EC" if self.current_theme == "Light" else "#1A1A2E"
            )
            row_frame.pack(fill="x", pady=3, padx=5)

            var = ctk.BooleanVar()
            cb = ctk.CTkCheckBox(row_frame, text=f"{f1}   ⇄   {f2}", variable=var)
            cb.pack(side="left", fill="x", expand=True, padx=(5, 0))

            preview_btn = ctk.CTkButton(
                row_frame, text="Preview", width=80,
                fg_color="#74C0FC", text_color="white",
                hover_color="#52B788",
                command=lambda path=f2: show_preview_window(self, path)
            )
            preview_btn.pack(side="right", padx=5)

            self.checkbox_vars.append((var, f2))

    def update_scan_progress(self, path, scanned, total):
        percent = scanned / total
        self.progress.set(percent)
        elapsed = time.time() - self.start_time
        remaining = (elapsed / scanned * total - elapsed) if scanned > 0 else 0
        mins, secs = int(remaining // 60), int(remaining % 60)
        estimate = f"{mins}m {secs}s lagi" if remaining > 3 else "Sebentar lagi"
        self.info_label.configure(text=f"{scanned}/{total} file • Estimasi {estimate}")
        self.update_idletasks()

    def scan_finished(self, total_files, dup_count, seconds):
        self.info_label.configure(
            text=f"Selesai • {total_files} file • {dup_count} duplikat • {seconds:.2f} detik"
        )
        messagebox.showinfo(
            "Selesai",
            f"Scan selesai!\n\nTotal file: {total_files}\n"
            f"Duplikat ditemukan: {dup_count}\nWaktu: {seconds:.2f} detik"
        )

    def apply_filter(self):
        if not self.duplicates:
            messagebox.showwarning("Tidak ada data", "Scan dahulu sebelum filter.")
            return
        tipe = self.filter_var.get()
        self.filtered_duplicates = filter_duplicates(self.duplicates, tipe)
        self.show_duplicates_in_list(self.filtered_duplicates)
        self.info_label.configure(text=f"Filter: {tipe} • {len(self.filtered_duplicates)} ditemukan")

    def refresh_view(self):
        if self.duplicates:
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

    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)
        self.current_theme = mode
        if self.showing_about:
            self.toggle_about_page()
            self.toggle_about_page()
        else:
            self.show_home_page()


if __name__ == "__main__":
    app = DuplicateManagerApp()
    app.mainloop()
