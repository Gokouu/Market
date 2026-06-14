import sqlite3
import os
import sys

DB_NAME = "asp_data.db"
SCHEMA_FILE = "schema.sql"

def init_db():
    print(f"Initializing database: {DB_NAME}")
    try:
        conn = sqlite3.connect(DB_NAME)
        with open(SCHEMA_FILE, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

def verify_schema():
    print("Verifying schema integrity...")
    required_tables = ["market_ledger", "awakened_registry", "node_discovery_log"]
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        missing = []
        for table in required_tables:
            if table not in tables:
                missing.append(table)
        
        if missing:
            print(f"Verification FAILED. Missing tables: {', '.join(missing)}")
            return False
        else:
            print("Verification PASSED. All required tables exist.")
            # Check columns for market_ledger as a sample
            cursor.execute("PRAGMA table_info(market_ledger);")
            cols = [row[1] for row in cursor.fetchall()]
            expected_cols = ["auction_id", "item_id", "unit_price", "amount", "auction_type", "seller_name", "buyer_name", "expiration_date"]
            if all(c in cols for c in expected_cols):
                print("Column verification for 'market_ledger' PASSED.")
            else:
                print("Column verification for 'market_ledger' FAILED.")
                return False
            
            conn.close()
            return True
    except Exception as e:
        print(f"Error verifying schema: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            init_db()
        elif command == "verify":
            if verify_schema():
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            print("Unknown command. Use 'init' or 'verify'.")
    else:
        # Default behavior: init and then verify
        init_db()
        if not verify_schema():
            sys.exit(1)
