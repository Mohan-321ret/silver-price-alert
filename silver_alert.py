# silver_alert.py
# GitHub Actions – AuraGold Silver Buy/Sell Alert

import os
import requests

# ================= CONFIG =================
BUY_THRESHOLD = 180.0
SELL_THRESHOLD = 185.0

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

AURAGOLD_API = "https://auragold.in/api/metal-price"

# ================= FUNCTIONS =================
def get_silver_price():
    r = requests.get(AURAGOLD_API, timeout=10)
    r.raise_for_status()
    data = r.json()

    # Extract silver price
    silver_price = float(data["silver"]["price"])
    return silver_price

def notify(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

# ================= MAIN =================
price = get_silver_price()

if price <= BUY_THRESHOLD:
    notify(f"📉 BUY SILVER\nAuraGold Price: ₹{price}/gm")

elif price >= SELL_THRESHOLD:
    notify(f"📈 SELL SILVER\nAuraGold Price: ₹{price}/gm")
