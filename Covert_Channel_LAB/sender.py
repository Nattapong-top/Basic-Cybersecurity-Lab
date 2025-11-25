# sender.py
from scapy.all import *

# กำหนด IP ปลายทาง (เครื่องที่เราเปิด receiver.py รอไว้)
# **ป๋าอย่าลืมแก้ตรงนี้เป็น IP เครื่องตัวเองหรือเครื่องที่จะทดสอบนะครับ**
target_ip = "127.0.0.1" 

msg = input("ป๋าอยากส่งข้อความลับอะไร: ")
secret_payload = f"Covert:{msg}"

# สร้าง Packet แบบแซนด์วิช 3 ชั้น
# ชั้น 1: IP ระบุปลายทาง
# ชั้น 2: ICMP บอกว่าเป็น Ping
# ชั้น 3: Raw คือข้อมูลที่เรายัดไส้ลงไป
packet = IP(dst=target_ip)/ICMP()/Raw(load=secret_payload)

print(f"กำลังแอบส่งข้อมูล: {msg} ไปที่ {target_ip}")
send(packet, verbose=0)
print("ส่งเรียบร้อย!")