import subprocess

def apply_ftp_gateway_defense():
    print("[*] Applying FTP brute-force defense on R2 gateway...")

    # Flush only FORWARD chain (not INPUT/OUTPUT)
    subprocess.run(["iptables", "-F", "FORWARD"], check=True)

    # Drop connections from Internet to DMZ if more than 5 attempts in 60 seconds
    subprocess.run([
        "iptables", "-A", "FORWARD", "-p", "tcp", "--dport", "21",
        "-s", "10.2.0.2", "-d", "10.12.0.0/24",
        "-m", "recent", "--name", "ftpbrute", "--rcheck", "--seconds", "60", "--hitcount", "5",
        "-j", "DROP"
    ], check=True)

    # Track new connection attempts from Internet to DMZ FTP
    subprocess.run([
        "iptables", "-A", "FORWARD", "-p", "tcp", "--dport", "21",
        "-s", "10.2.0.2", "-d", "10.12.0.0/24",
        "-m", "recent", "--name", "ftpbrute", "--set",
        "-j", "ACCEPT"
    ], check=True)

    print("[+] FTP brute-force defense applied on R2.")

if __name__ == "__main__":
    apply_ftp_gateway_defense()

