"""
crypto_etl/main.py
Run:  python -m crypto_etl   OR   python -m crypto_etl.main
"""

import requests, csv, pathlib, datetime

API = "https://api.coingecko.com/api/v3/simple/price"
OUT = pathlib.Path("prices.csv")
COINS = ["bitcoin", "ethereum"]

def fetch():
    resp = requests.get(API, params={"ids": ",".join(COINS), "vs_currencies": "usd"})
    resp.raise_for_status()
    data = resp.json()
    ts = datetime.datetime.utcnow().isoformat(timespec="seconds")
    return [(ts, coin, data[coin]["usd"]) for coin in COINS]

def save(rows):
    exists = OUT.exists()
    with OUT.open("a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["timestamp", "coin", "price_usd"])
        w.writerows(rows)

if __name__ == "__main__":
    save(fetch())
    print("Row appended:", fetch())
