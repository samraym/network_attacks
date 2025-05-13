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
* **Ping (ICMP)** and **SSH (port 22)** are allowed for local administration.


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
```
sudo -E python3 topo.py
```
All .nft firewall scripts will be executed on the correct nodes directly from the Python script.

## attacks

### network scans







---








