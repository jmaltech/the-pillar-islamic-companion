import customtkinter as customtk

from app_sections.qibla import get_qibla_data


class QiblaFrame(customtk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.container = customtk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, pady=20, padx=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        self.title_label = customtk.CTkLabel(
            self.container,
            text="Qibla Finder",
            font=customtk.CTkFont(size=26, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.input_label = customtk.CTkLabel(
            self.container,
            text="City, State, or ZIP Code:",
            font=customtk.CTkFont(size=14)
        )
        self.input_label.grid(row=1, column=0, padx=15, pady=10, sticky="e")

        self.location_entry = customtk.CTkEntry(
            self.container,
            width=200,
            placeholder_text="e.g. Nashville, TN"
        )
        self.location_entry.grid(row=1, column=1, padx=15, pady=10, sticky="w")

        self.search_btn = customtk.CTkButton(
            self.container,
            text="Find Qibla Direction",
            font=customtk.CTkFont(size=15, weight="bold"),
            height=38,
            command=self.run_qibla_search
        )
        self.search_btn.grid(row=2, column=0, columnspan=2, pady=20)

        self.results_box = customtk.CTkTextbox(
            self.container,
            width=380,
            height=220,
            font=customtk.CTkFont(family="Consolas", size=13),
            state="disabled"
        )
        self.results_box.grid(row=3, column=0, columnspan=2, pady=(5, 20))

    def run_qibla_search(self):
        location = self.location_entry.get().strip()

        if not location:
            self.display_message("Error: Please enter a location.")
            return

        self.display_message("Connecting to location services...\nPlease wait.")
        self.update()

        result = get_qibla_data(location)

        if not result.get("success"):
            self.display_message(f"Error: {result.get('error')}")
        else:
            report = (
                f"--- QIBLA RESULT ---\n\n"
                f"Location          : {result['location']}\n"
                f"Coordinates       : {result['latitude']}, {result['longitude']}\n"
                f"-----------------------------------------\n"
                f"Qibla Bearing     : {result['qibla_degrees']}°\n"
                f"Compass Direction : {result['qibla_direction']}\n"
                f"-----------------------------------------\n\n"
                f"Face approximately {result['qibla_degrees']} degrees clockwise\n"
                f"from true north."
            )
            self.display_message(report)

    def display_message(self, message):
        self.results_box.configure(state="normal")
        self.results_box.delete("0.0", "end")
        self.results_box.insert("0.0", message)
        self.results_box.configure(state="disabled")
