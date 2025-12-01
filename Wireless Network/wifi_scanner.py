from scapy.all import *

# สร้าง set ไว้เก็บ MAC Address ของ Wi-Fi ที่เจอแล้ว (จะได้ไม่ปริ้นท์ซ้ำ)
ap_list = set()

def packet_handler(packet):
    # ตรวจสอบว่า Packet นี้มีชั้นข้อมูล 802.11 Beacon หรือไม่?
    # Dot11Beacon คือสัญญาณที่ Router ปล่อยออกมาบอกว่า "ฉันชื่อนี้นะ"
    if packet.haslayer(Dot11Beacon):
        
        # ดึง MAC Address ของตัวส่ง (BSSID)
        # addr2 ในโครงสร้าง 802.11 คือ Source Address
        bssid = packet[Dot11].addr2
        
        # เช็คว่าเคยเจอตัวนี้หรือยัง ถ้ายังให้ทำงานต่อ
        if bssid not in ap_list:
            try:
                # ดึงชื่อ SSID (ชื่อ Wi-Fi)
                # Dot11Elt คือ Element ข้อมูลต่างๆ
                # ID 0 หมายถึง SSID, ID 1 หมายถึง Rates, ID 3 หมายถึง Channel ฯลฯ
                # info คือข้อมูลข้างใน (ชื่อ Wi-Fi)
                ssid = packet[Dot11Elt].info.decode('utf-8')
            except:
                ssid = "<อ่านไม่ออก/Hidden>"

            # เพิ่มลงรายการที่เจอแล้ว
            ap_list.add(bssid)
            
            # ดึง Channel (ต้องวนลูปหา Element ID 3)
            # (ส่วนนี้ซับซ้อนหน่อย ผมละไว้ก่อน เอาแค่ชื่อกับ MAC)
            
            print(f"[+] เจอ Wi-Fi ใหม่: {ssid:20} | MAC: {bssid}")

# เริ่มสแกน
print("กำลังสแกนหา Wi-Fi (กด Ctrl+C เพื่อหยุด)...")
# iface ต้องใส่ชื่อ Interface Wi-Fi ของเรา (ถ้าใน Kali มักเป็น wlan0 หรือ wlan0mon)
# บน Windows ถ้าไม่ใส่ iface มันจะพยายามเดา (แต่อาจจะไม่เจอ Beacon)
sniff(prn=packet_handler, store=0)