# Albion Stream Parser (ASP) - Engine

Passive network-sniffing engine for Albion Online.

## Project Structure

- `db/`: Database schema and initialization scripts.
  - `schema.sql`: SQLite schema definition.
  - `init_db.py`: CLI tool to initialize and verify the database.
- `engine/`: Packet sniffing and parsing logic (Modules A, B, C).
- `shared/`: Shared types and constants.

## Database Setup

To initialize the database, run:

```bash
cd db
python3 init_db.py
```

To verify schema integrity:

```bash
cd db
python3 init_db.py verify
```
