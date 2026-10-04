import customtkinter as customtk

from app_sections.prayer_schedule import (
    get_coordinates,
    get_prayer_times,
    format_prayer_list,
    get_hijri_date,
    format_full_date
)


class PrayerFrame(customtk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.container = customtk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, pady=20, padx=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        self.title_label = customtk.CTkLabel(
            self.container,
            text="Islamic Prayer Times",
            font=customtk.CTkFont(size=26, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 5))

        self.date_label = customtk.CTkLabel(
            self.container,
            text=f"{format_full_date()}  |  {get_hijri_date()}",
            font=customtk.CTkFont(size=14, slant="italic")
        )
        self.date_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

        self.input_label = customtk.CTkLabel(
            self.container,
            text="City, State, or ZIP Code:",
            font=customtk.CTkFont(size=14)
        )
        self.input_label.grid(row=2, column=0, padx=15, pady=10, sticky="e")

        self.location_entry = customtk.CTkEntry(
            self.container,
            width=200,
            placeholder_text="e.g. Nashville, TN"
        )
        self.location_entry.grid(row=2, column=1, padx=15, pady=10, sticky="w")

        self.search_btn = customtk.CTkButton(
            self.container,
            text="Get Prayer Schedule",
            font=customtk.CTkFont(size=15, weight="bold"),
            height=38,
            command=self.run_prayer_search
        )
        self.search_btn.grid(row=3, column=0, columnspan=2, pady=20)

        self.results_box = customtk.CTkTextbox(
            self.container,
            width=380,
            height=260,
            font=customtk.CTkFont(family="Consolas", size=14),
            state="disabled"
        )
        self.results_box.grid(row=4, column=0, columnspan=2, pady=(5, 20))

    def run_prayer_search(self):
        location = self.location_entry.get().strip()

        if not location:
            self.display_message("Error: Please enter a location.")
            return

        self.display_message("Fetching location data and calculating times...\nPlease wait.")
        self.update()

        coords_info, error = get_coordinates(location)

        if error:
            self.display_message(f"Error: {error}")
            return

        latitude, longitude, city_state = coords_info
        prayers_obj = get_prayer_times(latitude, longitude)

        if not prayers_obj:
            self.display_message("Error: Could not calculate prayer times for this location.")
            return

        prayer_list = format_prayer_list(prayers_obj)

        report = (
            f"--- DAILY PRAYER SCHEDULE ---\n\n"
            f"Location: {city_state}\n"
            f"-----------------------------------------\n"
        )

        for prayer in prayer_list:
            report += f"{prayer['name']:<15} {prayer['time']:>22}\n"

        report += "-----------------------------------------"
        self.display_message(report)

    def display_message(self, message):
        self.results_box.configure(state="normal")
        self.results_box.delete("0.0", "end")
        self.results_box.insert("0.0", message)
        self.results_box.configure(state="disabled")
