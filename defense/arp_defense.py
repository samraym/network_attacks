from scapy.all import sniff, ARP
import os

known_arp = {}

def handle_arp(pkt):
    # on veut juste check les paquets ARP 
    if pkt[ARP].op != 2: 
        return

    # ip et mac source du paquet ARP
    ip = pkt[ARP].psrc
    mac = pkt[ARP].hwsrc

    # check si on a déja vu cette adresse IP avec une adresse MAC différente
    if ip in known_arp and known_arp[ip] != mac:
        print(f"ARP SPOOF DETECTED: {ip} changed from {known_arp[ip]} to {mac}")
        # flush et restaure ARP
        os.system(f"ip neigh flush to {ip}")
    else:
        known_arp[ip] = mac

print("ARP Monitor running...")
sniff(filter="arp", prn=handle_arp, store=0)

