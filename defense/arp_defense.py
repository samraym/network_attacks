# arp_defense.py
from scapy.all import sniff, ARP
import os

known_arp = {}

def handle_arp(pkt):
    if pkt[ARP].op != 2:  # only ARP replies
        return

    ip = pkt[ARP].psrc
    mac = pkt[ARP].hwsrc

    if ip in known_arp and known_arp[ip] != mac:
        print(f"[!] ARP SPOOF DETECTED: {ip} changed from {known_arp[ip]} to {mac}")
        # Flush and restore ARP
        os.system(f"ip neigh flush to {ip}")
    else:
        known_arp[ip] = mac

print("[*] ARP Monitor running...")
sniff(filter="arp", prn=handle_arp, store=0)

