# receiver.py
from scapy.all import *

def process_packet(packet):
    # เช็คว่าเป็น ICMP ประเภท Request (Ping เข้ามา) และมีข้อมูล (Raw layer) หรือไม่
    if packet.haslayer(ICMP) and packet[ICMP].type == 8 and packet.haslayer(Raw):
        # ดึงข้อมูลออกมา (Payload)
        payload = packet[Raw].load
        
        # แปลงข้อมูลจาก byte เป็น string
        try:
            message = payload.decode('utf-8')
            
            # เช็ครหัสลับ ถ้าเจอคำว่า "Covert:" แสดงว่าเป็นพวกเดียวกัน
            if message.startswith("Covert:"):
                actual_msg = message.replace("Covert:", "")
                print(f"[+] ได้รับข้อความลับจาก {packet[IP].src}: {actual_msg}")
                
        except:
            pass # ถ้าแกะไม่ออก หรือไม่ใช่ข้อความเรา ก็ปล่อยผ่าน

print("กำลังดักฟัง Ping... (กด Ctrl+C เพื่อหยุด)")
# sniff คือคำสั่งดักจับ packet 
# filter="icmp" คือบอกให้สนใจแค่ ping
sniff(filter="icmp", prn=process_packet)