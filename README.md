# Albion Stream Parser (ASP) - Engine

Passive network-sniffing engine for Albion Online.

## Project Structure

- `db/`: Database schema and initialization scripts.
  - `schema.sql`: SQLite schema definition.
  - `init_db.py`: CLI tool to initialize and verify the database.
- `engine/`: Packet sniffing and parsing logic (Modules A, B, C).
  - `sniffer.py`: Passive network listener prototype.
- `shared/`: Shared types and constants.

## Phase 1: Passive Network Ingestion Prototype
The engine uses a passive network listener to intercept Albion Online UDP packets (port 5056) without attaching to the game process.

### Features
- **Passive Sniffing**: Uses `libpcap` and `scapy` for non-intrusive data capture.
- **Strict Regex Parsing**: Implements a balanced bracket parser to isolate JSON payloads (`{"Id":...}`) mixed with corrupted binary noise.
- **Clean Debug Logger**: Outputs raw hex and extracted text for verification.

### Usage
To run the sniffer prototype (requires root):
```bash
sudo python3 engine/sniffer.py --iface eth0
```

To test with fake packets:
```bash
sudo python3 engine/test_sender.py
```

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
