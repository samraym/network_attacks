# network_attacks - homework LINFO2347
### basis enterprise network protection

on utilise une politique de défense en profondeur (defense in depth).
Configurer des pare-feux sur chaque composant de l’architecture réseau :  
- Serveurs en **DMZ** (HTTP, FTP, DNS, NTP)
- Routeur **R1** (accès Workstations)
- Routeur **R2** (accès Internet)

---

## 🖥️ Structure du réseau

| Composant | Rôle                         | Interface(s) concernée(s) |
|-----------|------------------------------|----------------------------|
| `http`    | Serveur web (port 80)        | DMZ                        |
| `ftp`     | Serveur FTP/SSH(ports 21,22) | DMZ                        |
| `dns`     | Serveur DNS (port 53)        | DMZ                        |
| `ntp`     | Serveur NTP (port 123)       | DMZ                        |
| `r1`      | Routeur vers WSs             | DMZ / WSs                  |
| `r2`      | Routeur vers Internet        | DMZ / Internet             |

---

## 🔒 Règles générales appliquées

- Politique **DROP** par défaut (`policy drop`) sur tous les `input` et `forward`.
- Acceptation uniquement des **flux nécessaires**.
- **Anti-DOS** via limitation de requêtes (dans FTP par exemple).
- Gestion des **connexions établies et connexes** (`ct state`).

---

## 📂 Fichiers de configuration

| Fichier     | Description                             |
|-------------|-----------------------------------------|
| `http.nft`  | Autorise uniquement ports 80, 22, ICMP  |
| `ftp.nft`   | Autorise FTP avec limitation DoS   |
| `dns.nft`   | Autorise port 53 (UDP/TCP)              |
| `ntp.nft`   | Autorise port 123 + SSH/ICMP            |
| `r1.nft`    | Contrôle accès WSs → DMZ/WWW            |
| `r2.nft`    | Contrôle accès DMZ → Internet           |

---


## attacks

### network scans





