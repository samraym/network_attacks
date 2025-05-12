#code bash qui execute tout les firewall
#chmod +x load_firewalls.sh
#./firewalls.sh

#!/bin/bash

# Exécute chaque script nftables dans l’ordre
echo "Chargement des firewalls..."

sudo nft -f http.nft && echo "[OK] http.nft"
sudo nft -f ftp.nft && echo "[OK] ftp.nft"
sudo nft -f dns.nft && echo "[OK] dns.nft"
sudo nft -f ntp.nft && echo "[OK] ntp.nft"
sudo nft -f r1.nft && echo "[OK] r1.nft"
sudo nft -f r2.nft && echo "[OK] r2.nft"

echo "Tous les firewalls ont été appliqués."
