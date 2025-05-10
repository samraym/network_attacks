#!/usr/bin/env python3


from scapy.all import IP, TCP, UDP, sr1, ICMP
from datetime import datetime



# IPs à scanner
DMZ_IPS = ["10.12.0.10","10.12.0.20","10.12.0.30","10.12.0.40"]
WORKSTATION_IPS = ["10.1.0.2","10.1.0.3"]

# Plage de ports
PORT_START = 20
PORT_END = 100

# Fichier de sortie
OUTPUT_FILE = "scan_results.txt"

# -------------------------------------------

def tcp_syn_scan(ip, port):
    pkt = IP(dst=ip)/TCP(dport=port, flags='S')
    resp = sr1(pkt, timeout=1, verbose=0)
    if resp is not None and resp.haslayer(TCP) and resp[TCP].flags == 18: 
        #resp is not None = recu une reponse // resp.haslayer(TCP) = contient segment TCP
        # resp[TCP].flags == 18 = correspond à SYN + ACK (port ouvert)
        return True
    return False

def udp_scan(ip, port):
    pkt = IP(dst=ip)/UDP(dport=port)
    resp = sr1(pkt, timeout=2, verbose=0)
    if resp is None:
        # Pas de réponse -> potentiellement ouvert ou bloqué
        return True
    elif resp.haslayer(ICMP) and resp[ICMP].type == 3 and resp[ICMP].code == 3: #port fermé 
        #resp[ICMP].type == 3 = destination unreachable. // resp[ICMP].code == 3 = port unreachable.
        return False
    else:
        return True

def scan_ip(ip, start_port, end_port):
    results = []
    for port in range(start_port, end_port + 1):
        if tcp_syn_scan(ip, port):
            results.append(f"TCP {port} OPEN")
        if udp_scan(ip, port):
            results.append(f"UDP {port} OPEN")
    return results

def run_full_scan():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Scan started at {timestamp}\n\n")

        for category, ip_list in [("DMZ", DMZ_IPS), ("Workstations", WORKSTATION_IPS)]:
            f.write(f"===== {category} =====\n")
            for ip in ip_list:
                f.write(f"\n[+] Results for {ip}:\n")
                results = scan_ip(ip, PORT_START, PORT_END)
                if results:
                    for line in results:
                        f.write(f"{line}\n")
                else:
                    f.write("No open ports found.\n")
            f.write("\n")

    print(f"[✓] Scan finished. Results saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    run_full_scan()

