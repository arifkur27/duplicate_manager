import customtkinter as ctk

class AboutFrame(ctk.CTkFrame):
    def __init__(self, parent):
        
        # Warna utama (tema)
        self.primary_color = "#5A5BF3"
        self.accent_color = "#6C63FF"
        self.text_secondary = "#444"
        self.bg_light = "#F8F9FA"
        self.bg_dark = "#1E1E2E"
        self.divider_color = "#DADCE0"

        # Tema adaptif
        current_theme = ctk.get_appearance_mode()
        bg_color = self.bg_dark if current_theme == "Dark" else self.bg_light
        subtext_color = "#DDE1E7" if current_theme == "Dark" else self.text_secondary

        # Inisialisasi Frame (Penting: Panggil super().__init__ hanya sekali)
        super().__init__(parent, fg_color=bg_color) 

        # Judul utama
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

        # Garis pemisah
        ctk.CTkFrame(self, height=2, fg_color=self.divider_color).pack(fill="x", padx=60, pady=(0, 20))

        # Tombol navigasi
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(pady=(0, 10))

        self.btn_info = ctk.CTkButton(
            nav_frame, text="Informasi Aplikasi",
            corner_radius=8, fg_color=self.primary_color,
            hover_color=self.accent_color, text_color="white",
            command=self.show_info
        )
        self.btn_info.grid(row=0, column=0, padx=10)

        self.btn_usage = ctk.CTkButton(
            nav_frame, text="Cara Penggunaan",
            corner_radius=8, fg_color=self.primary_color,
            hover_color=self.accent_color, text_color="white",
            command=self.show_usage
        )
        self.btn_usage.grid(row=0, column=1, padx=10)

        self.btn_team = ctk.CTkButton(
            nav_frame, text="Pembuat Aplikasi",
            corner_radius=8, fg_color=self.primary_color,
            hover_color=self.accent_color, text_color="white",
            command=self.show_team
        )
        self.btn_team.grid(row=0, column=2, padx=10)

        # Frame utama konten (scrollable FIX)
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=15,
            fg_color=("white", "#2B2B40")
        )
        self.content_frame.pack(padx=30, pady=(10, 25), fill="both", expand=True)

        # Default tampilan
        self.show_info() 

        # Footer
        ctk.CTkLabel(
            self,
            text="Versi 1.0.0 — Dibuat oleh Kelompok 5",
            font=("Poppins", 12, "italic"),
            text_color=subtext_color
        ).pack(pady=(0, 10))

    # ======================================================
    # LOGIKA HALAMAN
    # ======================================================
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_info(self):
        self.clear_content()
        
        current_theme = ctk.get_appearance_mode()
        text_color_adapt = "#E0E0E0" if current_theme == "Dark" else "#1B1B2F"

        ctk.CTkLabel(
            self.content_frame,
            text="Informasi Aplikasi",
            font=("Poppins", 18, "bold"),
            text_color=self.primary_color
        ).pack(pady=(15, 10))

        ctk.CTkLabel(
            self.content_frame,
            text=("Duplicate File Manager adalah aplikasi berbasis GUI yang membantu Anda "
                      "mendeteksi file duplikat di komputer dengan cepat dan efisien. "
                      "Aplikasi ini dirancang dengan antarmuka modern, mudah digunakan, "
                      "dan mendukung mode aman (*Safe Mode*) agar file tidak langsung terhapus permanen."),
            font=("Inter", 13),
            text_color=text_color_adapt,
            justify="left",
            wraplength=600
        ).pack(padx=25, pady=(0, 15))

        fitur_text = (
            "• Pencarian file duplikat berdasarkan nama, ukuran, atau hash.\n"
            "• Filter berdasarkan jenis file (gambar, musik, dokumen, dll).\n"
            "• Mode aman (*Safe Mode*) untuk menghindari penghapusan permanen.\n"
            "• Antarmuka ringan, cepat, dan ramah pengguna."
        )

        ctk.CTkLabel(
            self.content_frame,
            text="Fitur Utama:",
            font=("Poppins", 14, "bold"),
            text_color=self.primary_color
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self.content_frame,
            text=fitur_text,
            font=("Inter", 13),
            text_color=text_color_adapt,
            justify="left"
        ).pack(padx=25, pady=(0, 10))

    def show_usage(self):
        self.clear_content()
        
        current_theme = ctk.get_appearance_mode()
        text_color_adapt = "#E0E0E0" if current_theme == "Dark" else "#1B1B2F"
        
        ctk.CTkLabel(
            self.content_frame,
            text="Cara Penggunaan",
            font=("Poppins", 18, "bold"),
            text_color=self.primary_color
        ).pack(pady=(15, 5))

        usage_text = (
            "1. Pilih folder yang ingin dipindai dari komputer Anda.\n"
            "2. Klik tombol **Cari Duplikat** untuk memulai proses pencarian.\n"
            "3. Setelah hasil muncul, centang file yang ingin dihapus.\n"
            "4. Tekan **Hapus File Terpilih** untuk membersihkan penyimpanan.\n"
            "5. Gunakan **Filter File** untuk menampilkan jenis file tertentu sesuai kebutuhan.\n\n"
            "💡 Tips tambahan:\n"
            "- Aktifkan *Safe Mode* agar file dipindahkan ke folder aman sebelum dihapus permanen.\n"
            "- Anda dapat meninjau ulang file di tab *Preview* sebelum dihapus.\n"
            "- Pastikan memiliki ruang kosong yang cukup saat melakukan pemindaian folder besar."
        )

        textbox = ctk.CTkTextbox(
            self.content_frame,
            width=600,
            height=200,
            font=("Inter", 13),
            wrap="word",
            fg_color=("#FFFFFF", "#2B2B40"),
            text_color=text_color_adapt,
            corner_radius=10
        )
        textbox.pack(padx=25, pady=(10, 15))
        textbox.insert("1.0", "\n" + usage_text)
        textbox.configure(state="disabled")

    def show_team(self):
        self.clear_content()
        
        current_theme = ctk.get_appearance_mode()
        text_color_adapt = "#E0E0E0" if current_theme == "Dark" else "#1B1B2F"

        ctk.CTkLabel(
            self.content_frame,
            text="Pembuat Aplikasi",
            font=("Poppins", 18, "bold"),
            text_color=self.primary_color
        ).pack(pady=(15, 10))

        team_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        team_frame.pack(padx=20, pady=(5, 15), fill="x", expand=True) 

        anggota = [
            ("Arif Kurniawan", "230103126"),
            ("Nasywa Hamna Zakiya", "230103146"),
            ("Dista Dian Saputri", "230103131"),
            ("Muhammad Ridwan Martana Putra", "230103144"),
            ("Muhammad Fadlan Al Farid", "230103199"),
        ]

        # Konfigurasi kolom agar simetris
        team_frame.grid_columnconfigure(0, weight=1)
        team_frame.grid_columnconfigure(1, weight=1)

        for i, (nama, nim) in enumerate(anggota):
            row = i // 2
            col = i % 2
            
            CARD_HEIGHT = 80 
            
            card = ctk.CTkFrame(
                team_frame,
                corner_radius=12,
                fg_color=("#FFFFFF", "#2F2F44"),
                border_color=self.accent_color,
                border_width=1,
                height=CARD_HEIGHT
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew") 

            ctk.CTkLabel(
                card,
                text=nama,
                font=("Poppins", 14, "bold"),
                text_color=self.primary_color
            ).pack(pady=(10, 2))

            ctk.CTkLabel(
                card,
                text=f"NIM: {nim}",
                font=("Inter", 13),
                text_color=text_color_adapt
            ).pack(pady=(0, 10))

        ctk.CTkLabel(
            self.content_frame,
            text="Universitas Duta Bangsa Surakarta — 2025",
            font=("Poppins", 12, "italic"),
            text_color=self.accent_color
        ).pack(pady=(10, 10))