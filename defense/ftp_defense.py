import subprocess

def apply_ftp_gateway_defense():
    print("Applying FTP brute-force defense on R2 gateway...")

    subprocess.run(["iptables", "-F", "FORWARD"], check=True)

    # on drop les connexions depuis Internet vers DMZ si on voit plus de 5 essais en 60 secondes
    subprocess.run([
        "iptables", "-A", "FORWARD", "-p", "tcp", "--dport", "21",
        "-s", "10.2.0.2", "-d", "10.12.0.0/24",
        "-m", "recent", "--name", "ftpbrute", "--rcheck", "--seconds", "60", "--hitcount", "5",
        "-j", "DROP"
    ], check=True)

    # on traque les nouvelles tentatives de connexions de Internet vers FTP
    subprocess.run([
        "iptables", "-A", "FORWARD", "-p", "tcp", "--dport", "21",
        "-s", "10.2.0.2", "-d", "10.12.0.0/24",
        "-m", "recent", "--name", "ftpbrute", "--set",
        "-j", "ACCEPT"
    ], check=True)

    print("FTP brute-force defense applied on R2.")

if __name__ == "__main__":
    apply_ftp_gateway_defense()

