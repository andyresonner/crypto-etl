import sqlite3, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DB   = ROOT / "warehouse" / "prices.db"

def init_db():
    schema = (ROOT / "warehouse" / "schema.sql").read_text()
    with sqlite3.connect(DB) as cx:
        cx.executescript(schema)

def append_prices(rows):
    """
    rows = list of dicts  {ts, coin, price_usd}
    """
    with sqlite3.connect(DB) as cx:
        cx.executemany(
            "INSERT OR IGNORE INTO prices(ts, coin, price_usd) VALUES (:ts, :coin, :price_usd)",
            rows,
        )
