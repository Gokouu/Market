-- Albion Stream Parser (ASP) - SQLite Schema

-- Table 1: market_ledger
-- Logs historical market depth for pricing analysis.
CREATE TABLE IF NOT EXISTS market_ledger (
    auction_id INTEGER PRIMARY KEY,
    item_id TEXT NOT NULL,           -- e.g., T4_RUNE or T8_HEAD_LEATHER_SET3@1
    unit_price INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    auction_type TEXT NOT NULL,      -- offer or request
    seller_name TEXT,                -- NULLABLE
    buyer_name TEXT,                 -- NULLABLE
    expiration_date TEXT NOT NULL    -- ISO-8601 string
);

-- Table 2: awakened_registry
-- Stores inspected high-tier gear profiles.
CREATE TABLE IF NOT EXISTS awakened_registry (
    item_guid TEXT PRIMARY KEY,
    crafter TEXT,
    owner TEXT,
    pvp_fame INTEGER,
    hp_modifier REAL,
    def_modifier REAL
);

-- Table 3: node_discovery_log
-- Tracks coordinates for open-world harvesting.
CREATE TABLE IF NOT EXISTS node_discovery_log (
    node_id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_type TEXT NOT NULL,         -- e.g., WISPS_RESOURCE_FIBER, RESOURCE_T7, FishingNodeSwarm
    timestamp INTEGER NOT NULL       -- Unix timestamp
);
