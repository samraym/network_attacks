import subprocess

def apply_ssh_gateway_defense():
    print("[*] Applying SSH brute-force defense on R2 gateway...")

    # Flush FORWARD chain (we're not touching INPUT here)
    subprocess.run(["iptables", "-F", "FORWARD"], check=True)

    # Drop IPs that exceeded SSH attempt threshold toward DMZ
    subprocess.run([
        "iptables", "-A", "FORWARD", "-p", "tcp", "--dport", "22",
        "-s", "10.2.0.2", "-d", "10.12.0.0/24",
        "-m", "recent", "--name", "sshbrute", "--rcheck", "--seconds", "60", "--hitcount", "5",
        "-j", "DROP"
    ], check=True)

    # Track new SSH attempts from Internet to DMZ
    subprocess.run([
        "iptables", "-A", "FORWARD", "-p", "tcp", "--dport", "22",
        "-s", "10.2.0.2", "-d", "10.12.0.0/24",
        "-m", "recent", "--name", "sshbrute", "--set",
        "-j", "ACCEPT"
    ], check=True)

    print("[+] SSH brute-force defense applied on R2.")

if __name__ == "__main__":
    apply_ssh_gateway_defense()

