"""
Fetch the latest BTC & ETH price, save to warehouse (SQLite) and to prices.csv,
then regenerate the PNG chart that GitHub Pages shows.

Run locally:
    python -m crypto_etl.main
It’s the same entry-point the GitHub Actions workflow calls.
"""
from datetime import datetime, timezone
from pathlib import Path
import csv
import json
import urllib.request

import matplotlib.pyplot as plt

from . import db   # our new helper ────────────────

ROOT = Path(__file__).resolve().parents[1]
WAREHOUSE = ROOT / "warehouse"
PRICES_CSV = ROOT / "prices.csv"
CHART_PNG = ROOT / "docs" / "chart.png"

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
}


def fetch_prices() -> list[dict]:
    """Return a list of rows {ts, coin, price_usd} for BTC & ETH (CoinGecko)."""
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum&vs_currencies=usd"
    )
    with urllib.request.urlopen(url, timeout=30) as fh:
        data = json.load(fh)

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = [
        {"ts": ts, "coin": COINS[k], "price_usd": float(v["usd"])}
        for k, v in data.items()
    ]
    return rows


def append_csv(rows: list[dict]) -> None:
    csv_exists = PRICES_CSV.exists()
    with PRICES_CSV.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["ts", "coin", "price_usd"])
        if not csv_exists:
            w.writeheader()
        w.writerows(rows)


def regenerate_chart() -> None:
    """Read the CSV and draw a simple price-history PNG for GitHub Pages."""
    # First, check if the CSV file exists and is not empty before trying to read it.
    if not PRICES_CSV.exists() or PRICES_CSV.stat().st_size == 0:
        print(f"'{PRICES_CSV}' not found or is empty. Skipping chart generation.")
        return  # Exit the function early

    import pandas as pd  # only used here

    df = pd.read_csv(PRICES_CSV, parse_dates=["ts"])
    
    # Add another check in case the file exists but has no data rows
    if df.empty:
        print(f"'{PRICES_CSV}' is empty after reading. Skipping chart generation.")
        return

    fig, ax = plt.subplots(figsize=(9, 5), dpi=120)
    for coin, grp in df.groupby("coin"):
        grp.plot(x="ts", y="price_usd", ax=ax, label=coin.lower())
    ax.set_ylabel("USD")
    ax.set_title("BTC & ETH price history (UTC)")
    fig.tight_layout()
    fig.savefig(CHART_PNG)
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    # 1 – ensure warehouse/db exists
    db.init_db()

    # 2 – fetch latest prices
    rows = fetch_prices()

    # 3 – append to SQLite + CSV
    db.append_prices(rows)
    append_csv(rows)

    # 4 – redraw chart for GitHub Pages
    regenerate_chart()


if __name__ == "__main__":
    main()
