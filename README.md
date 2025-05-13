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

The attack is launched from the Internet node and targets both DMZ servers and workstations. The script checks whether a port is open or closed and writes the results to the file `scan_results.txt`.

**Note:** The scan only targets the IPs `10.12.0.10`, `10.12.0.20`, `10.12.0.30`, `10.12.0.40`, `10.1.0.2`, and `10.1.0.3`, and ports ranging from **20 to 25**. The script could easily be extended to scan more ports or IPs, but this would take longer.

To launch the attack from Mininet, run:
```bash
internet python3 ./attacks/networkscan.py
```

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






