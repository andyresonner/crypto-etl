# plot.py — generate docs/chart.png from prices.csv
import pandas as pd, matplotlib.pyplot as plt
from pathlib import Path

CSV = Path("prices.csv")
DOCS = Path("docs")
DOCS.mkdir(exist_ok=True)

df = pd.read_csv(CSV)
pivot = df.pivot(index="timestamp", columns="coin", values="price_usd")

plt.figure(figsize=(8,4))
pivot.plot(ax=plt.gca())
plt.title("BTC & ETH price history (UTC)")
plt.ylabel("USD")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig(DOCS / "chart.png")
