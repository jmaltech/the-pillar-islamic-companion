import customtkinter as customtk

from app_sections.flashcards import FlashcardManager


class FlashcardsFrame(customtk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.flashcards = FlashcardManager()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = customtk.CTkLabel(
            self,
            text="Islamic Flashcards",
            font=customtk.CTkFont(size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=20)

        self.card_frame = customtk.CTkFrame(
            self, width=500, height=300, corner_radius=10
        )
        self.card_frame.grid(row=1, column=0, pady=20)
        self.card_frame.grid_propagate(False)
        self.card_frame.grid_rowconfigure(0, weight=1)
        self.card_frame.grid_columnconfigure(0, weight=1)

        self.flashcard_label = customtk.CTkLabel(
            self.card_frame,
            text=self.flashcards.get_current_text(),
            font=customtk.CTkFont(size=24, weight="bold"),
            wraplength=450
        )
        self.flashcard_label.grid(row=0, column=0)

        self.number_label = customtk.CTkLabel(
            self.card_frame,
            text=self.flashcards.get_current_number(),
            font=customtk.CTkFont(size=12, weight="bold"),
            wraplength=450
        )
        self.number_label.grid(row=1, column=0)

        self.button_frame = customtk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, pady=(0, 20))

        self.button_prev = customtk.CTkButton(
            self.button_frame,
            text="< Prev",
            width=80,
            command=self.on_prev_click
        )
        self.button_prev.grid(row=0, column=0, padx=10)

        self.button_flip = customtk.CTkButton(
            self.button_frame,
            text="FLIP",
            width=120,
            command=self.on_flip_click
        )
        self.button_flip.grid(row=0, column=1, padx=10)

        self.button_next = customtk.CTkButton(
            self.button_frame,
            text="Next >",
            width=80,
            command=self.on_next_click
        )
        self.button_next.grid(row=0, column=2, padx=10)

    def on_next_click(self):
        self.flashcards.next_card()
        self.refresh_display()

    def on_prev_click(self):
        self.flashcards.prev_card()
        self.refresh_display()

    def on_flip_click(self):
        self.flashcards.flip_card()
        self.refresh_display()

    def refresh_display(self):
        self.flashcard_label.configure(text=self.flashcards.get_current_text())
        self.number_label.configure(text=self.flashcards.get_current_number())
