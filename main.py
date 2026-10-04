# Importing the main GUI module
import customtkinter as customtk

# Importing custom views package
from views.home_ui import HomeFrame
from views.zakat_ui import ZakatFrame
from views.prayer_ui import PrayerFrame
from views.qibla_ui import QiblaFrame
from views.flashcards_ui import FlashcardsFrame

# Setting the custom appearance
customtk.set_appearance_mode("Dark")
customtk.set_default_color_theme("dark-blue")

# Main Class (Orchestrator)
class App(customtk.CTk):
    def __init__(self):
        super().__init__()

        self.title("The Pillar")
        self.geometry("900x600")
        self.minsize(600, 400)

        # 1 - MAIN WINDOW CONFIGURATION USING GRID SYSTEM
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)

        # 2 - SIDEBAR FRAME STUFF
        self.sidebar_frame = customtk.CTkFrame(self, width = 200, corner_radius = 0)
        self.sidebar_frame.grid(row = 0, column = 0, sticky = "nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight = 1)

        # 3 - ADD WIDGETS TO SIDEBAR
        self.logo_label = customtk.CTkLabel(self.sidebar_frame, text = "Companion App", font = customtk.CTkFont(size = 20, weight = "bold"))
        self.logo_label.grid(row = 0, column = 0, padx = 20, pady = (20,30))

        # 4 - BUTTONS (UPDATED TO WORK WITH FRAME SWAPING)
        self.button_home = customtk.CTkButton(self.sidebar_frame, text = "Home",
                                               command = lambda: self.select_frame("home"))
        self.button_home.grid(row = 1, column = 0, padx = 20, pady = (0, 100))
        
        self.button_zakat = customtk.CTkButton(self.sidebar_frame, text = "Zakat Calculator",
                                               command = lambda: self.select_frame("zakat"))
        self.button_zakat.grid(row = 2, column = 0, padx = 20, pady = 10)

        self.button_prayer_times = customtk.CTkButton(self.sidebar_frame, text = "Prayer Times",
                                                      command = lambda: self.select_frame("prayer"))
        self.button_prayer_times.grid(row = 3, column = 0, padx = 20, pady = 10)

        self.button_qibla = customtk.CTkButton(self.sidebar_frame, text = "The Qibla",
                                               command = lambda: self.select_frame("qibla"))
        self.button_qibla.grid(row = 4, column = 0, padx = 20, pady = 10)

        self.button_flashcards = customtk.CTkButton(self.sidebar_frame, text = "Islamic Flashcards",
                                                    command = lambda: self.select_frame("flashcards"))
        self.button_flashcards.grid(row = 5, column = 0, padx = 20, pady = 10)

        # 5 - CONTENT FRAMES (BROUGHT IN FROM VIEWS PACKAGE)
        self.home_frame = HomeFrame(self, corner_radius = 10)
        self.zakat_frame = ZakatFrame(self, corner_radius = 10)
        self.prayer_frame = PrayerFrame(self, corner_radius = 10)
        self.qibla_frame = QiblaFrame(self, corner_radius = 10)
        self.flashcards_frame = FlashcardsFrame(self, corner_radius = 10)

        self.select_frame("home")

    # FRAME SWAPPING FUNCTION
    def select_frame(self, name):
        self.home_frame.grid_forget()
        self.zakat_frame.grid_forget()
        self.prayer_frame.grid_forget()
        self.qibla_frame.grid_forget()
        self.flashcards_frame.grid_forget()

        if name == "home":
            self.home_frame.grid(row = 0, column = 1, sticky = "nsew", padx = 20, pady = 20)
        elif name == "zakat":
            self.zakat_frame.grid(row = 0, column = 1, sticky = "nsew", padx = 20, pady = 20)
        elif name == "prayer":
            self.prayer_frame.grid(row = 0, column = 1, sticky = "nsew", padx = 20, pady = 20)
        elif name == "qibla":
            self.qibla_frame.grid(row = 0, column = 1, sticky = "nsew", padx = 20, pady = 20)
        elif name == "flashcards":
            self.flashcards_frame.grid(row = 0, column = 1, sticky = "nsew", padx = 20, pady = 20)
            

if __name__ == "__main__":
    app = App()
    app.mainloop()
