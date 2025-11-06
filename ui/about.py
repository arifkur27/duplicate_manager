import customtkinter as ctk

class AboutFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Warna utama (otomatis adaptif)
        self.primary_color = "#5A5BF3"   # biru lembut
        self.accent_color = "#6C63FF"    # hover biru lembut
        self.text_main = "#1B1B2F"       # teks utama
        self.text_secondary = "#444"     # teks sekunder
        self.bg_light = "#F8F9FA"
        self.bg_dark = "#1E1E2E"
        self.divider_color = "#DADCE0"

        # Tentukan background sesuai tema
        current_theme = ctk.get_appearance_mode()
        bg_color = self.bg_dark if current_theme == "Dark" else self.bg_light
        text_color = "white" if current_theme == "Dark" else self.text_main
        subtext_color = "#DDE1E7" if current_theme == "Dark" else self.text_secondary

        super().__init__(parent, fg_color=bg_color)

        # Judul Utama
        ctk.CTkLabel(
            self,
            text="Duplicate File Manager",
            font=("Poppins", 26, "bold"),
            text_color=self.primary_color
        ).pack(pady=(25, 5))

        # Subjudul
        ctk.CTkLabel(
            self,
            text="Aplikasi untuk mendeteksi dan menghapus file duplikat secara cepat dan aman.",
            font=("Poppins", 14),
            text_color=subtext_color
        ).pack(pady=(0, 20))

        # Garis Pemisah
        ctk.CTkFrame(self, height=2, fg_color=self.divider_color).pack(fill="x", padx=60, pady=(0, 20))

        # Tombol Navigasi Mini (Informasi / Cara Pakai)
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(pady=(0, 10))

        self.btn_info = ctk.CTkButton(
            nav_frame,
            text="Informasi Aplikasi",
            corner_radius=8,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            text_color="white",
            command=self.show_info
        )
        self.btn_info.grid(row=0, column=0, padx=10)

        self.btn_usage = ctk.CTkButton(
            nav_frame,
            text="Cara Penggunaan",
            corner_radius=8,
            fg_color=self.primary_color,
            hover_color=self.accent_color,
            text_color="white",
            command=self.show_usage
        )
        self.btn_usage.grid(row=0, column=1, padx=10)

        # Frame Konten Utama
        self.content_frame = ctk.CTkFrame(self, corner_radius=15, fg_color=("white", "#2B2B40"))
        self.content_frame.pack(padx=30, pady=(10, 25), fill="both", expand=True)

        # Default tampilan
        self.show_info()

        # Footer
        ctk.CTkLabel(
            self,
            text="Versi 1.0.0 — Dibuat oleh Nasywa",
            font=("Poppins", 12, "italic"),
            text_color=subtext_color
        ).pack(pady=(0, 10))

    # ======================================================
    #                  LOGIKA HALAMAN
    # ======================================================
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_info(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content_frame,
            text="Informasi Aplikasi",
            font=("Poppins", 18, "bold"),
            text_color=self.primary_color
        ).pack(pady=(15, 10))

        ctk.CTkLabel(
            self.content_frame,
            text=(
                "Duplicate File Manager adalah aplikasi berbasis GUI yang membantu Anda "
                "mendeteksi file duplikat di komputer dengan cepat dan efisien. "
                "Aplikasi ini dirancang dengan antarmuka modern, mudah digunakan, "
                "dan mendukung mode aman (*Safe Mode*) agar file tidak langsung terhapus permanen."
            ),
            font=("Inter", 13),
            text_color="#E0E0E0" if ctk.get_appearance_mode() == "Dark" else "#1B1B2F",
            justify="left",
            wraplength=600
        ).pack(padx=25, pady=(0, 15))

        ctk.CTkLabel(
            self.content_frame,
            text="Fitur Utama:",
            font=("Poppins", 14, "bold"),
            text_color=self.primary_color
        ).pack(pady=(10, 5))

        fitur_text = (
            "• Pencarian file duplikat berdasarkan nama, ukuran, atau hash.\n"
            "• Filter berdasarkan jenis file (gambar, musik, dokumen, dll).\n"
            "• Mode aman (*Safe Mode*) untuk menghindari penghapusan permanen.\n"
            "• Antarmuka ringan, cepat, dan ramah pengguna."
        )

        ctk.CTkLabel(
            self.content_frame,
            text=fitur_text,
            font=("Inter", 13),
            text_color="#E0E0E0" if ctk.get_appearance_mode() == "Dark" else "#1B1B2F",
            justify="left"
        ).pack(padx=25, pady=(0, 10))

    def show_usage(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content_frame,
            text="Cara Penggunaan",
            font=("Poppins", 18, "bold"),
            text_color=self.primary_color
        ).pack(pady=(15, 10))

        usage_text = (
            "1. Pilih folder yang ingin dipindai dari komputer Anda.\n"
            "2. Klik tombol **Cari Duplikat** untuk memulai proses pencarian.\n"
            "3. Setelah hasil muncul, centang file yang ingin dihapus.\n"
            "4. Tekan **Hapus File Terpilih** untuk membersihkan penyimpanan.\n"
            "5. Gunakan **Filter File** untuk menampilkan jenis file tertentu sesuai kebutuhan."
        )

        ctk.CTkLabel(
            self.content_frame,
            text=usage_text,
            font=("Inter", 13),
            text_color="#E0E0E0" if ctk.get_appearance_mode() == "Dark" else "#1B1B2F",
            justify="left",
            wraplength=600
        ).pack(padx=25, pady=(0, 15))

        ctk.CTkLabel(
            self.content_frame,
            text="💡 Tips: Aktifkan *Safe Mode* agar file dipindahkan ke folder aman sebelum dihapus permanen.",
            font=("Poppins", 12, "italic"),
            text_color=self.accent_color
        ).pack(pady=(10, 10))

