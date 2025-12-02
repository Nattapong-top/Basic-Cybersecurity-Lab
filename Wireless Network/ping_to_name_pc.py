import socket

target_ip = "10.1.102.29"

try:
    # สั่งถามชื่อเครื่อง (Hostname) จาก IP
    hostname, alias, ip = socket.gethostbyaddr(target_ip)
    print(f"[*] จับตัวได้แล้ว! เจ้าของ IP {target_ip} คือ: {hostname}")
except Exception as e:
    print(f"[!] หาชื่อไม่เจอครับ: {e}")