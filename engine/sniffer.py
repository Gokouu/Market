import re
import scapy.all as scapy
import sys
import argparse

def extract_json(data):
    """
    Extracts balanced JSON-like blocks starting with {"Id":
    to handle corrupted binary noise as per ASP specifications.
    """
    # Search for potential JSON starts
    for match in re.finditer(b'\\{"Id":', data):
        start = match.start()
        count = 0
        for i in range(start, len(data)):
            if data[i] == ord('{'):
                count += 1
            elif data[i] == ord('}'):
                count -= 1
            
            if count == 0:
                # Found a balanced block
                yield data[start:i+1]
                break

def packet_callback(packet):
    if packet.haslayer(scapy.UDP):
        payload = bytes(packet[scapy.UDP].payload)
        
        # Clean Debug Logger: Raw Hex (Requirement)
        # We only print the first 64 bytes to avoid cluttering, 
        # but the full hex is available in the payload.
        print(f"[DEBUG] Raw Payload (hex): {payload[:64].hex()}...")
        
        # Extract JSON blocks using the regex-based balanced parser
        found = False
        for json_block in extract_json(payload):
            try:
                decoded = json_block.decode('utf-8', errors='ignore')
                print(f"[JSON] {decoded}")
                found = True
            except Exception as e:
                print(f"[ERROR] Failed to decode block: {e}")
        
        if not found:
            # If no JSON found, maybe it's a non-JSON packet or binary part
            # We still log the text representation for verification
            text_rep = payload.decode('utf-8', errors='ignore')
            # Filter out non-printable characters for the 'clean' logger
            clean_text = "".join(c if c.isprintable() else "." for c in text_rep)
            print(f"[DEBUG] Clean Text: {clean_text[:128]}...")

def main():
    parser = argparse.ArgumentParser(description="ASP Passive Network Listener Prototype")
    parser.add_argument("--iface", default="eth0", help="Interface to listen on (default: eth0)")
    parser.add_argument("--port", type=int, default=5056, help="UDP port to filter (default: 5056)")
    args = parser.parse_args()

    print(f"ASP Passive Network Listener Prototype starting...")
    print(f"Operational Mode: PASSIVE SNIFFING ONLY")
    print(f"Listening on {args.iface}, UDP port {args.port}...")
    
    try:
        # Use Scapy to sniff. 
        # Note: Must run as root or with CAP_NET_RAW.
        scapy.sniff(iface=args.iface, filter=f"udp port {args.port}", prn=packet_callback, store=0)
    except PermissionError:
        print("ERROR: Permission denied. Please run as root (sudo).")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
