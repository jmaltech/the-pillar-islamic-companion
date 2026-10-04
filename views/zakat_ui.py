import customtkinter as customtk

from app_sections.zakat_calculator import (
    fetch_precious_metal_prices,
    calculate_precious_metals_value,
    calculate_gross_assets,
    calculate_net_wealth,
    calculate_nisab_threshold,
    calculate_zakah_due
)


class ZakatFrame(customtk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.container = customtk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, pady=20, padx=20)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        self.title_label = customtk.CTkLabel(
            self.container,
            text="Islamic Zakah Calculator",
            font=customtk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        self.entries = {}

        def create_input_row(label_text, row_num, default_val="0.0"):
            label = customtk.CTkLabel(self.container, text=label_text)
            label.grid(row=row_num, column=0, padx=10, pady=5, sticky="e")

            entry = customtk.CTkEntry(self.container, placeholder_text=default_val)
            entry.insert(0, default_val)
            entry.grid(row=row_num, column=1, padx=10, pady=5, sticky="w")
            return entry

        self.entries['gold'] = create_input_row("Gold Held (grams):", 1)
        self.entries['silver'] = create_input_row("Silver Held (grams):", 2)
        self.entries['cash'] = create_input_row("Cash & Bank Balances ($):", 3)
        self.entries['investments'] = create_input_row("Investments & Crypto ($):", 4)
        self.entries['inventory'] = create_input_row("Business Inventory ($):", 5)
        self.entries['receivables'] = create_input_row("Money Owed to You ($):", 6)
        self.entries['debts'] = create_input_row("Short-term Debts ($):", 7)

        self.calc_btn = customtk.CTkButton(
            self.container,
            text="Calculate Zakah",
            command=self.run_calculation
        )
        self.calc_btn.grid(row=8, column=0, columnspan=2, pady=20)

        self.results_box = customtk.CTkTextbox(
            self.container,
            width=350,
            height=240,
            state="disabled"
        )
        self.results_box.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        self.market_prices = fetch_precious_metal_prices()

    def run_calculation(self):
        try:
            gold_g = float(self.entries['gold'].get())
            silver_g = float(self.entries['silver'].get())
            cash = float(self.entries['cash'].get())
            investments = float(self.entries['investments'].get())
            inventory = float(self.entries['inventory'].get())
            receivables = float(self.entries['receivables'].get())
            debts = float(self.entries['debts'].get())

            metals_val = calculate_precious_metals_value(
                gold_g,
                silver_g,
                self.market_prices['gold_per_gram'],
                self.market_prices['silver_per_gram']
            )

            gross = calculate_gross_assets(
                cash, metals_val, investments, inventory, receivables
            )
            net = calculate_net_wealth(gross, debts)
            nisab = calculate_nisab_threshold(
                self.market_prices['gold_per_gram'],
                self.market_prices['silver_per_gram'],
                standard="silver"
            )
            result = calculate_zakah_due(net, nisab)

            report = (
                f"--- ZAKAH REPORT ---\n\n"
                f"Gross Zakatable Assets: ${gross:,.2f}\n"
                f"Deductible Liabilities: -${debts:,.2f}\n"
                f"----------------------------------\n"
                f"Net Zakatable Wealth: ${result['net_wealth']:,.2f}\n"
                f"Nisab Threshold (Silver): ${result['nisab_threshold']:,.2f}\n\n"
            )

            if result['is_eligible']:
                report += (
                    f"NISAB MET: YES\n"
                    f"Total Zakah Due (2.5%): ${result['zakah_due']:,.2f}\n\n"
                    f"You meet the Nisab threshold."
                )
            else:
                report += (
                    f"NISAB MET: NO\n"
                    f"Total Zakah Due: $0.00\n\n"
                    f"Zakah is not obligatory for you this year."
                )

            self.results_box.configure(state="normal")
            self.results_box.delete("0.0", "end")
            self.results_box.insert("0.0", report)
            self.results_box.configure(state="disabled")

        except ValueError:
            self.results_box.configure(state="normal")
            self.results_box.delete("0.0", "end")
            self.results_box.insert(
                "0.0",
                "Error: Please enter valid numbers in all fields."
            )
            self.results_box.configure(state="disabled")
