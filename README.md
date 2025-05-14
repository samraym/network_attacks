# network_attacks - homework LINFO2347
## basis enterprise network protection

We apply a **defense-in-depth** strategy by configuring multiple layers of firewalls within the network. The following components are protected by custom firewall rules:

* Servers in the **DMZ** (HTTP, FTP, DNS, NTP)
* Router **R1** (access to Workstations)
* Router **R2** (access to Internet)

---

### `r1.nft` – Firewall for Workstations 

This firewall controls the incoming and outgoing traffic for the workstations (`10.1.0.0/24`).

* The workstations can send **ping** and **initiate connections** towards the **DMZ servers** (`10.12.0.0/24`), the **Internet** (`10.2.0.0/24`) and other **workstations** (`10.1.0.0/24`)
* Responses to these connections are allowed.
* Unsolicited incoming connections to workstations are **blocked**.
*  Allows SSH and ping to R2.


### `dns.nft, ftp.nft, http.nft, ntp.nft ` – Firewalls for DMZ servers

those firewalls controls the incoming and outgoing traffic for the DMZ servers.
the firewalls :
* Allows responses to existing connections.
* Blocks any outgoing connection, including ping.
* Loopback traffic is allowed.
* Applies default drop policies on all chains.

### `r2.nft` – Firewall for internet
This firewall controls the incoming and outgoing traffic for internet (`10.2.0.0/24`).

* Allows connections initiated from the DMZ or Workstations to the Internet.
* Allows the Internet to initiate connections only to the DMZ.
* Blocks all incoming connections from the Internet to the Workstations.
* Allows SSH and ping to R2.


### execute every firewall on the VM

We have modified the topo.py file to automatically deploy all firewall configurations once the topology is created.

We added a custom function:
```
apply_firewalls(net: Mininet)
```
This function is called after the Mininet topology is initialized, and it applies all the firewall rules to the appropriate nodes.

To launch the topology and apply firewalls:
```bash
sudo -E python3 topo.py
```
All .nft firewall scripts will be executed on the correct nodes directly from the Python script.

## Attacks

### network scans

We have implemented a Python script named networkscan.py capable of performing a network scan in two different ways:

- **TCP SYN port scan**
- **UDP port scan**

The attack is launched from the Internet node and targets both DMZ servers and workstations. The script checks whether a port is open or closed and writes the results to the file `scan_results.txt`. The script allows you to choose the target IP address and specify the range of ports to scan, from a starting port to an ending port.
To launch the attack from Mininet, run:
```bash
internet python3 ./attacks/networkscan.py IP_address start_port end_port
```
exemple :
```bash
internet python3 ./attacks/networkscan.py 10.12.0.10 20 30
```

###  ARP Poisoning

For the ARP cache poisoning attack, the attack is configured to work with `ws2` as the attacker, `r1` as the gateway and `ws3` as the victim. However, you can easily modify your target in the script by modifying the global variables **victim_ip** and **gateway_ip**. In our specific case, **`ws2`** impersonates the router (`r1`) to the victim machine **`ws3`**. Our script sends **spoofed ARP replies** to `ws3`, tricking it into associating the IP address of the gateway (`10.1.0.1`) with the MAC address of the attacker (`ws2`). As a result, all traffic from `ws3` destined to the gateway is sent to `ws2`.

To run the attack:
```bash
ws2 python3 ./attacks/arp_poison.py
```
To observe the effect:
* Open a terminal in ws3

Run:
* ping 10.1.0.1  (`r1`) 
* ping 10.1.0.2  (`ws2`)
* arp -n

You will see that both IPs now resolve to the same MAC address.

###  FTP Brute-force Attack

To prepare the attack:

* A user named victim is added on the FTP server with the weak password **lovely**

To create that user we ran on our VM:
```bash
ftp adduser victim
```

The brute-force attack targets the FTP server (`10.12.0.40`) in the DMZ because we know from network scanning that the port 21 is open. The attack script named `ftp_bruteforce.py` systematically attempts to log in using a known weak username (`victim`) and a wordlist of common passwords (`10k-most-common.txt`).


To run the attack:
```bash
internet python3 ./attacks/ftp_bruteforce.py
```
The attack is launched from the **Internet** node, simulating an external attacker traversing `r2` to reach the DMZ. The script will try all passwords in the wordlist until it successfully authenticates. For our example, successful login is printed as:

* **FOUND: victim:lovely**

It's then possible from **Internet** to log into the FTP server using the found credentials. 
```bash
ftp 10.12.0.40
```


### SSH Brute-force Attack

Here, we decided to provide an alternative to the ftp bruteforce attack. It's a brute-force attack targeting the SSH service of the HTTP server (`10.12.0.10`) also launched from the **Internet**. The script named `ssh_bruteforce.py` iterates over the same wordlist as the FTP bruteforce (`10k-most-common.txt`) to guess the password of a specific user (`victim`). 

To launch the attack:

```bash
internet python3 ./attacks/ssh_bruteforce.py
```

The script will try all passwords in the wordlist until it successfully authenticates. For our example, successful login is printed as:

* **FOUND: victim:lovely**

If successful, it allows the attacker to establish an SSH session using:

```bash
ssh victim@10.12.0.10
```

### Reflected DNS DoS Attack

For this attack, we aimed to do a reflected Denial of Service where the DNS server is exploited to flood `ws3` with unsolicited responses. Since the **Internet** cannot directly reach the workstations due to firewall rules, the attacker spoofs the source IP address of the victim (`ws3`) and sends crafted DNS requests to the DNS server (`10.12.0.20`). For the requests, we decided to use various DNS record types (A, AAAA, MX, TXT, CNAME, etc.) to increase the processing load on the DNS server.

Each request appears to come from `ws3`. The DNS server then thinks that it should send all the replies back to `ws3`. This results in a high volume of traffic being redirected to the victim (`ws3`).

To launch the attack:
```bash
internet python3 ./attacks/reflected_dos.py
```

To observe the attack in action, open two terminals and run:
```bash
ws3 tcpdump -i ws3-eth0 udp -n -vv
dns tcpdump -i dns-eth0 udp -n -vv
```

You will see a stream of DNS packets generated by the attack and redirected to the workstation via the DNS server. 

---

## Defense 
### network scans defense
The basic firewall configuration already provides good protection against **UDP port scans**. For **TCP port scans**, we implemented an additional firewall called `scan_defense.nft`.
This firewall builds upon the rules from `r2.nft` and adds scan protection:
* Limits TCP SYN packets from the Internet to the DMZ to 30 packets per minute
* Limits UDP traffic from the Internet to DMZ to 30 packets per minute

From within Mininet, run the following command to apply the firewall on R2:
```bash
r2 nft -f ./defense/scan_defense.nft
```

### ARP Poisoning defense

To mitigate ARP spoofing attacks, we implemented a monitoring script named `arp_defense.py` that passively observes incoming ARP replies on the victim host (in our case `ws3`). It detects suspicious changes in **IP-to-MAC** associations and flushes the corresponding ARP entry if a spoof is suspected.

#### How to run the defense

1. (Optional) Clean your ARP cache beforehand:
```bash
ws3 arp -d <IP>
```
2. Run the script
```bash
ws3 python3 ./defense/arp_defense.py
```

Once the ARP monitoring is in place, you can try to ping `10.1.0.1` from `ws3` and you'll notice that it doesn't appear in the ARP table and a waning message spotting the spoof will be displayed. 

Example of warning message: 

```bash
ARP SPOOF DETECTED: 10.1.0.1 changed from c6:ee:e1:d6:df:fb to e6:b4:81:40:67:bf
```

###  FTP Brute-force defense

To counter brute-force attempts from the Internet targeting the FTP server, we implemented a rate-limiting defense directly on `r2` which acts as the gateway between the **Internet** and the internal topology.

The script uses iptables to:

* Track each new connection attempt from `10.2.0.2` (`Internet`) to any server in `10.12.0.0/24` on port `21` (FTP).

* Drop traffic if more than 5 login attempts are detected in 60 seconds from the same **IP**.

To deploy the defense, execute:
```bash
r2 python3 ./defense/ftp_defense.py
```

When the defense is activated, the bruteforce attack will have a timeout on each guess and the password won't be recovered.

### SSH Bruteforce Defense

To protect the DMZ servers from SSH brute-force attacks originating from the **Internet**, we implemented a defense script on the `r2` gateway named `ssh_protect.py`. Similarly to `ftp_defense.py`, the script uses iptables to monitor and limit the number of SSH login attempts from a single **IP** address. If more than 5 attempts are detected within 60 seconds from the same **IP**, the following SSH traffic from that source is dropped.

To launch the defense mechanism:
```bash
r2 python3 ./defense/ssh_protect.py
```

Once the protection is set, the ssh brute force script won't work anymore. It will automatically be stopped after two passwords tries.

### Reflected DNS DoS defense

To mitigate the reflected DNS DoS attack, we implemented a protection script to apply on `r1`, the router between the DMZ and the workstations. This script uses iptables to drop unsolicited UDP packets from the DNS server (`10.12.0.20`) to the workstations (`10.1.0.0/24`) on port **5353** (`DNS`).

The protection allows normal DNS traffic initiated by the workstations but blocks any spoofed DNS responses crafted to target a workstation like `ws3`. After applying this protection, re-running the attack results in 0 packets reaching `ws3`.

To apply the defense, execute:

```bash
r1 python3 ./defense/reflected_dos_protect.py
```


