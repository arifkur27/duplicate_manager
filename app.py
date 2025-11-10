import customtkinter as ctk
from ui.main_window import DuplicateManagerApp

if __name__ == "__main__":
    # Atur tema default saat aplikasi dimulai
    ctk.set_appearance_mode("Dark")  # Atau "Light"
    ctk.set_default_color_theme("blue")
    
    app = DuplicateManagerApp()
    app.mainloop()