import sqlite3
from pathlib import Path

# This finds the root directory of your project
ROOT = Path(__file__).resolve().parents[1]

# This sets up the path to your warehouse directory and the database file
WAREHOUSE = ROOT / "warehouse"
DB_FILE = WAREHOUSE / "prices.db"


def init_db() -> None:
    """Create the SQLite database and prices table if they don't exist."""
    # Ensure the warehouse directory exists
    WAREHOUSE.mkdir(exist_ok=True)
    
    # Connect to the database (it will be created if it doesn't exist)
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    
    # Create the 'prices' table if it's not already there.
    # The column names now match main.py
    cur.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            timestamp TEXT,
            coin TEXT,
            price_usd REAL
        )
    """)
    
    # Save the changes and close the connection
    con.commit()
    con.close()


def append_prices(rows: list[dict]) -> None:
    """Append new price rows to the prices table in the database."""
    # Connect to the database
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    
    # Prepare the data for insertion
    # This now correctly looks for 'timestamp' instead of 'ts'
    data_to_insert = [
        (row['timestamp'], row['coin'], row['price_usd']) for row in rows
    ]
    
    # Insert all the new rows at once
    cur.executemany("INSERT INTO prices VALUES (?, ?, ?)", data_to_insert)
    
    # Save the changes and close the connection
    con.commit()
    con.close()
