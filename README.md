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

those firewalls controls controls the incoming and outgoing traffic for the DMZ servers.
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

## attacks

### network scans

We have implemented a Python script name networkscan.py capable of performing a network scan in two different ways:

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

### ARP Poisoning

We implemented an ARP cache poisoning attack where **`ws2`** impersonates the router (`r1`) to the victim machine **`ws3`**. The script sends **spoofed ARP replies** to `ws3`, tricking it into associating the IP address of the gateway (`10.1.0.1`) with the MAC address of the attacker (`ws2`). As a result, all traffic from `ws3` destined to the gateway is mistakenly sent to `ws2`.

To run the attack:
```bash
ws2 python3 ./attacks/arp_poison.py
```
To observe the effect:
* Open a terminal in ws3
Run:
* ping 10.1.0.1  # router
* ping 10.1.0.2  # attacker

You will see that both IPs now resolve to the same MAC address, confirming that the ARP table has been poisoned.

This validates the effectiveness of the attack and shows how `ws3` can intercept or redirect traffic intended for the router.
## defense 
### network scans
The basic firewall configuration already provides good protection against **UDP port scans**. For **TCP port scans**, we implemented an additional firewall called `scan_defense.nft`.
This firewall builds upon the rules from `r2.nft` and adds scan protection:
* Limits TCP SYN packets from the Internet to the DMZ to 30 packets per minute
* Limits UDP traffic from the Internet to DMZ to 30 packets per minute

From within Mininet, run the following command to apply the firewall on R2:
```bash
r2 nft -f ./defense/scan_defense.nft
```






