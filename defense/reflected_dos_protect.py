import subprocess

def apply_reflected_dns_defense():
    print("Applying defense against reflected DNS DoS on r1...")

    # flush les forward rules
    subprocess.run(["iptables", "-F", "FORWARD"], check=True)

    # ok ppur connexion légitimes et normales
    subprocess.run([
        "iptables", "-A", "FORWARD",
        "-m", "conntrack", "--ctstate", "ESTABLISHED,RELATED",
        "-j", "ACCEPT"
    ], check=True)

    # Drop les paquets udp non voulu depuis le DNS serveur vers les workstations sur le port 5353
    subprocess.run([
        "iptables", "-A", "FORWARD", "-p", "udp",
        "-s", "10.12.0.20", "-d", "10.1.0.0/24", "--sport", "5353",
        "-m", "conntrack", "--ctstate", "NEW",
        "-j", "DROP"
    ], check=True)

    # of pour réponse
    subprocess.run([
        "iptables", "-A", "FORWARD",
        "-s", "10.1.0.0/24", "-d", "10.12.0.0/24",
        "-j", "ACCEPT"
    ], check=True)

    subprocess.run([
        "iptables", "-A", "FORWARD",
        "-s", "10.12.0.0/24", "-d", "10.1.0.0/24",
        "-m", "conntrack", "--ctstate", "ESTABLISHED,RELATED",
        "-j", "ACCEPT"
    ], check=True)

    print("Reflected DNS DoS protection applied on r1")

if __name__ == "__main__":
    apply_reflected_dns_defense()

