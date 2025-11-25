from scapy.all import *
import time

target_ip = "127.0.0.1" # ยิงใส่ตัวเอง

print(f"กำลังยิง SYN รัวๆ ไปที่ {target_ip}")

# วนลูปยิง 20 นัด
for i in range(20):
    # สร้าง Packet ปลอม (S = SYN)
    packet = IP(dst=target_ip)/TCP(dport=80, flags="S")
    send(packet, verbose=0)
    print(f"ยิงนัดที่ {i+1}")
    time.sleep(0.1) # ยิงเร็วๆ