# Zakah Calculator Module
# Course: High-Level Language - Python Group Project
# Description: Modules to fetch live precious metal prices, aggregate zakatable
#              assets and debts, check Nisab eligibility, and compute Zakah due.

import urllib.request
import json
from typing import Dict, Union

TROY_OUNCE_TO_GRAMS = 31.1034768
SILVER_NISAB_GRAMS = 612.36
GOLD_NISAB_GRAMS = 87.48
ZAKAH_RATE = 0.025


def fetch_precious_metal_prices() -> Dict[str, Union[float, bool]]:
    fallback_data = {
        "gold_per_gram": 137.22,
        "silver_per_gram": 2.02,
        "is_live": False
    }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    try:
        gold_url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
        req_gold = urllib.request.Request(gold_url, headers=headers)
        with urllib.request.urlopen(req_gold, timeout=5) as response:
            gold_data = json.loads(response.read().decode('utf-8'))
            gold_price_oz = gold_data['chart']['result'][0]['meta']['regularMarketPrice']

        silver_url = "https://query1.finance.yahoo.com/v8/finance/chart/SI=F"
        req_silver = urllib.request.Request(silver_url, headers=headers)
        with urllib.request.urlopen(req_silver, timeout=5) as response:
            silver_data = json.loads(response.read().decode('utf-8'))
            silver_price_oz = silver_data['chart']['result'][0]['meta']['regularMarketPrice']

            return {
                "gold_per_gram": round(gold_price_oz / TROY_OUNCE_TO_GRAMS, 2),
                "silver_per_gram": round(silver_price_oz / TROY_OUNCE_TO_GRAMS, 2),
                "is_live": True
            }
    except Exception:
        return fallback_data


def calculate_precious_metals_value(
    gold_grams: float,
    silver_grams: float,
    gold_price_per_g: float,
    silver_price_per_g: float
) -> float:
    gold_val = max(0.0, gold_grams) * gold_price_per_g
    silver_val = max(0.0, silver_grams) * silver_price_per_g
    return round(gold_val + silver_val, 2)


def calculate_gross_assets(
    cash: float,
    metals_value: float,
    investments: float,
    business_inventory: float,
    receivables: float
) -> float:
    assets = [cash, metals_value, investments, business_inventory, receivables]
    return round(sum(max(0.0, float(a)) for a in assets), 2)


def calculate_net_wealth(gross_assets: float, debts_and_liabilities: float) -> float:
    net = gross_assets - max(0.0, float(debts_and_liabilities))
    return round(max(0.0, net), 2)


def calculate_nisab_threshold(
    gold_price_per_g: float,
    silver_price_per_g: float,
    standard: str = "silver"
) -> float:
    if standard.lower() == "gold":
        return round(GOLD_NISAB_GRAMS * gold_price_per_g, 2)
    return round(SILVER_NISAB_GRAMS * silver_price_per_g, 2)


def calculate_zakah_due(net_wealth: float, nisab_threshold: float) -> Dict[str, Union[float, bool]]:
    is_eligible = net_wealth >= nisab_threshold
    zakah_amount = round(net_wealth * ZAKAH_RATE, 2) if is_eligible else 0.0

    return {
        "is_eligible": is_eligible,
        "net_wealth": net_wealth,
        "nisab_threshold": nisab_threshold,
        "zakah_due": zakah_amount
    }


def prompt_float_input(prompt_message: str) -> float:
    while True:
        try:
            value = float(input(prompt_message))
            if value < 0:
                print("Value cannot be negative. Please enter 0 or a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numerical value.")


def run_zakah_calculator_cli():
    print("\n        ISLAMIC ZAKAH CALCULATOR (USD)        ")

    print("\nFetching live market rates for Gold and Silver")
    prices = fetch_precious_metal_prices()

    status_str = "Live Data" if prices["is_live"] else "Offline Estimate"
    print(f"Status: [{status_str}]")
    print(f"Gold Spot Price   : ${prices['gold_per_gram']:.2f} / gram")
    print(f"Silver Spot Price : ${prices['silver_per_gram']:.2f} / gram")

    print("\n- Step 1: Enter Precious Metals Holdings -")
    gold_g = prompt_float_input("Enter total weight of Gold held (in grams): ")
    silver_g = prompt_float_input("Enter total weight of Silver held (in grams): ")

    metals_val = calculate_precious_metals_value(
        gold_g, silver_g, prices['gold_per_gram'], prices['silver_per_gram']
    )

    print("\n- Step 2: Enter Financial & Liquid Assets (USD) -")
    cash = prompt_float_input("Cash on hand & Bank account balances: $")
    investments = prompt_float_input("Stocks, Mutual Funds, Crypto, 401k/IRA (accessible): $")
    inventory = prompt_float_input("Business inventory / goods held for trade: $")
    receivables = prompt_float_input("Money owed to you expected to be repaid: $")

    gross_assets = calculate_gross_assets(
        cash=cash,
        metals_value=metals_val,
        investments=investments,
        business_inventory=inventory,
        receivables=receivables
    )

    print("\n- Step 3: Enter Deductible Debts & Liabilities -")
    debts = prompt_float_input("Short-term debts & immediate expenses due this year: $")

    net_wealth = calculate_net_wealth(gross_assets, debts)

    nisab_standard = "silver"
    nisab_value = calculate_nisab_threshold(
        prices['gold_per_gram'], prices['silver_per_gram'], standard=nisab_standard
    )

    result = calculate_zakah_due(net_wealth, nisab_value)

    print("\n                ZAKAH REPORT                ")
    print(f"\nGross Zakatable Assets    : ${gross_assets:,.2f}")
    print(f"Deductible Liabilities    : -${debts:,.2f}")
    print("---------------------------------------------")
    print(f"Net Zakatable Wealth      : ${result['net_wealth']:,.2f}")
    print(f"Nisab Threshold ({nisab_standard.title()})  : ${result['nisab_threshold']:,.2f}")
    print("---------------------------------------------")

    if result['is_eligible']:
        print("Nisab Met                 : Yes")
        print(f"Total Zakah Due (2.5%)    : ${result['zakah_due']:,.2f}")
        print("\nYou meet the Nisab threshold. May Allah bless your wealth and charity!\n")
    else:
        diff = result['nisab_threshold'] - result['net_wealth']
        print("Nisab Met                 : No")
        print("Total Zakah Due           : $0.00")
        print(f"\nYour net wealth is ${diff:,.2f} below the Nisab threshold.")
        print("Zakah is not obligatory for you this year.\n")


if __name__ == "__main__":
    run_zakah_calculator_cli()
