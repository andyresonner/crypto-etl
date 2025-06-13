[![Hourly ETL](https://github.com/andyresonner/crypto-etl/actions/workflows/etl.yml/badge.svg)](https://github.com/andyresonner/crypto-etl/actions/workflows/etl.yml)
# crypto-etl

Hourly Bitcoin & Ethereum price ETL — built with **GitHub Actions**

![Price chart](https://andyresonner.github.io/crypto-etl/chart.png)

## How it works
1. Action runs every hour (`cron`)
2. Fetches BTC & ETH prices from CoinGecko  
3. Appends to `prices.csv`
4. Regenerates `docs/chart.png`
5. Auto-commits both files back to **main**

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m crypto_etl.main       # update prices.csv
python plot.py                  # refresh chart.png
