from scapy.all import *
import time

def send_fake_packet():
    # Albion Online often has JSON payloads in its UDP stream (simplified for testing)
    fake_json = '{"Id":123,"AuctionType":"offer","ItemTypeId":"T4_RUNE","UnitPrice":120000,"Amount":5,"TotalPrice":600000}'
    # Adding some binary noise before and after as per spec
    payload = b'\x01\x02\x03' + fake_json.encode() + b'\x04\x05\x06'
    
    print(f"Sending fake Albion packet to port 5056...")
    packet = IP(dst="127.0.0.1")/UDP(sport=12345, dport=5056)/Raw(load=payload)
    send(packet, verbose=False)

if __name__ == "__main__":
    send_fake_packet()
