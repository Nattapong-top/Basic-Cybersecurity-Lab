from scapy.all import *
from collections import defaultdict

# --- ส่วนตั้งค่า (Config) ---
# ใส่ IP ที่เราเชื่อถือ (เช่น IP เครื่องตัวเอง) เพื่อไม่ให้มันแจ้งเตือนมั่ว
# ป๋าเอา IP เครื่องป๋าที่ขึ้นในรูปเมื่อกี้ (10.1.102.28) มาใส่ตรงนี้ครับ
WHITELIST_IPS = ["127.0.0.1", "10.1.102.28", "192.168.1.1"] 

# จำนวนครั้งที่ยอมให้เชื่อมต่อได้ ก่อนจะเริ่มโวยวาย (ปรับให้สูงขึ้นเพื่อลด False Positive)
ALERT_THRESHOLD = 50 

# ตัวแปรเก็บสถิติ
ip_count = defaultdict(int)

def detect_syn_flood(packet):
    # ตรวจสอบว่าเป็น TCP และมี Flag 'S' (SYN)
    if packet.haslayer(TCP) and packet[TCP].flags == 'S':
        src_ip = packet[IP].src
        dst_port = packet[TCP].dport
        
        # 1. เช็ค Whitelist: ถ้าเป็นพวกเดียวกัน ให้ปล่อยผ่านเลย ไม่ต้องนับ
        if src_ip in WHITELIST_IPS:
            return 

        # 2. นับจำนวนการเชื่อมต่อ
        ip_count[src_ip] += 1
        
        # 3. ถ้าจำนวนเกินกำหนด ให้แจ้งเตือน!
        if ip_count[src_ip] > ALERT_THRESHOLD:
            print(f"*** [เตือนภัย] IP: {src_ip} ส่ง SYN มาถล่ม {ip_count[src_ip]} ครั้งแล้ว! (เป้าหมาย Port: {dst_port}) ***")
            
        # (Optional) ถ้าอยากเห็น Log แบบ Realtime ว่ามีใครเข้ามาบ้าง (แต่ไม่เตือน) ให้เอา # ข้างล่างออก
        # else:
        #     print(f"[-] รับ SYN จาก {src_ip} -> Port {dst_port} (ครั้งที่ {ip_count[src_ip]})")

# เริ่มทำงาน
print(f"--- ระบบเฝ้าระวัง SYN Flood V.2 (Whitelisted: {len(WHITELIST_IPS)} IPs) ---")
print(f"จะแจ้งเตือนเมื่อมีการเชื่อมต่อเกิน {ALERT_THRESHOLD} ครั้ง")
print("กำลังทำงาน... (กด Ctrl+C เพื่อหยุด)")

# sniff() จะดักจับ Packet ไปเรื่อยๆ
sniff(filter="tcp", prn=detect_syn_flood, store=0)