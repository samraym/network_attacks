#!/usr/bin/env python3

import argparse
from scapy.all import IP, TCP, UDP, sr1, ICMP
from datetime import datetime

# Fichier de sortie
OUTPUT_FILE = "scan_results.txt"

# -------------------------------------------

def tcp_syn_scan(ip, port):
    pkt = IP(dst=ip)/TCP(dport=port, flags='S')
    resp = sr1(pkt, timeout=1, verbose=0)
    return resp is not None and resp.haslayer(TCP) and resp[TCP].flags == 18

def udp_scan(ip, port):
    pkt = IP(dst=ip)/UDP(dport=port)
    resp = sr1(pkt, timeout=2, verbose=0)
    if resp is None:
        return True  # potentiellement ouvert ou bloqué
    elif resp.haslayer(ICMP) and resp[ICMP].type == 3 and resp[ICMP].code == 3:
        return False  # fermé
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

def run_scan(ip, start_port, end_port):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Scan started at {timestamp} for {ip} (ports {start_port}-{end_port})\n\n")
        f.write(f"[+] Results for {ip}:\n")
        results = scan_ip(ip, start_port, end_port)
        for line in results:
            f.write(f"{line}\n")
    print(f"[✓] Scan finished. Results saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP/UDP port scanner")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("start_port", type=int, help="Start port")
    parser.add_argument("end_port", type=int, help="End port")
    args = parser.parse_args()

    run_scan(args.ip, args.start_port, args.end_port)
