-- warehouse/schema.sql
CREATE TABLE IF NOT EXISTS prices (
    ts        TIMESTAMP PRIMARY KEY,
    coin      TEXT NOT NULL,
    price_usd NUMERIC NOT NULL
);
