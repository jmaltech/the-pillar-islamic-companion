# Importing the main GUI module
import customtkinter as customtk


class HomeFrame(customtk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.home_label = customtk.CTkLabel(
            self,
            text="Welcome! Select any tool from the left.",
            font=customtk.CTkFont(size=24)
        )
        self.home_label.pack(expand=True)
