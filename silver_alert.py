# silver_alert.py
# GitHub Actions – AuraGold Silver Buy/Sell Alert (NO Selenium)

import os
import requests
import re

# ================= CONFIG =================
BUY_THRESHOLD = 180.0
SELL_THRESHOLD = 185.0

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

AURAGOLD_URL = "https://auragold.in"

# Regex to capture prices like ₹186.47/gm
PRICE_REGEX = re.compile(r"₹\s*([0-9]+(?:\.[0-9]+)?)\s*/\s*gm")

# ================= FUNCTIONS =================
def notify(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    r.raise_for_status()

def get_silver_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-IN,en;q=0.9",
    }

    r = requests.get(AURAGOLD_URL, headers=headers, timeout=15)
    r.raise_for_status()

    matches = PRICE_REGEX.findall(r.text)

    if len(matches) < 2:
        raise RuntimeError("Could not extract silver price from AuraGold page")

    # AuraGold page order:
    # [gold_price, silver_price]
    silver_price = float(matches[-1])
    return silver_price

# ================= MAIN =================
price = get_silver_price()

if price <= BUY_THRESHOLD:
    notify(f"📉 BUY SILVER\nAuraGold Price: ₹{price}/gm")

elif price >= SELL_THRESHOLD:
    notify(f"📈 SELL SILVER\nAuraGold Price: ₹{price}/gm")
