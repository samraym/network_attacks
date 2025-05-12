#!/usr/bin/env python3

from scapy.all import IP, TCP, UDP, sr1, ICMP
from datetime import datetime
import ipaddress

# Sous-réseaux à scanner
SUBNETS = ["10.1.0.0/24", "10.12.0.0/24"]

# Plage de ports
PORT_START = 20
PORT_END = 23

# Fichier de sortie
OUTPUT_FILE = "scan_results.txt"

def tcp_syn_scan(ip, port):
    pkt = IP(dst=ip)/TCP(dport=port, flags='S')
    resp = sr1(pkt, timeout=1, verbose=0)
    return resp is not None and resp.haslayer(TCP) and resp[TCP].flags == 0x12

def udp_scan(ip, port):
    pkt = IP(dst=ip)/UDP(dport=port)
    resp = sr1(pkt, timeout=2, verbose=0)
    if resp is None:
        return True  # Pas de réponse = potentiellement ouvert ou filtré
    elif resp.haslayer(ICMP) and resp[ICMP].type == 3 and resp[ICMP].code == 3:
        return False  # Port inaccessible => fermé
    return True

def scan_ip(ip, start_port, end_port):
    results = []
    for port in range(start_port, end_port + 1):
        if tcp_syn_scan(ip, port):
            results.append(f"TCP {port} OPEN")
        else:
            results.append(f"TCP {port} CLOSED")

        if udp_scan(ip, port):
            results.append(f"UDP {port} OPEN/BLOCKED")
        else:
            results.append(f"UDP {port} CLOSED")
    return results

def run_full_scan():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Scan started at {timestamp}\n\n")

        for subnet in SUBNETS:
            f.write(f"===== Subnet {subnet} =====\n")
            for ip in ipaddress.IPv4Network(subnet):
                if str(ip).endswith(".0") or str(ip).endswith(".255"):
                    continue  # Ignore adresse réseau et broadcast
                f.write(f"\n[+] Results for {ip}:\n")
                results = scan_ip(str(ip), PORT_START, PORT_END)
                for line in results:
                    f.write(f"{line}\n")
            f.write("\n")

    print(f"[✓] Scan finished. Results saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    run_full_scan()
