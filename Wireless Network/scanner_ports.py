import socket
from datetime import datetime

# รายชื่อประตู (Port) ยอดฮิตที่ IT Support ต้องรู้
# ป๋าสามารถเพิ่มเลขอื่นที่อยากรู้เข้าไปในลิสต์นี้ได้เลย
COMMON_PORTS = {
    21: "FTP (ส่งไฟล์)",
    22: "SSH (รีโมทแบบจอดำ)",
    23: "Telnet (รีโมทแบบโบราณ)",
    53: "DNS (แปลงชื่อเว็บ)",
    80: "HTTP (เว็บไซต์)",
    443: "HTTPS (เว็บปลอดภัย)",
    445: "SMB (แชร์ไฟล์ Windows)",
    3389: "RDP (Remote Desktop)",
    8080: "Web Proxy/Alt Web",
    9100: "Printer Port" # อันนี้สำคัญ! ถ้าเจอคือเครื่องปริ้นท์ชัวร์
}

def scan_ports(target_ip):
    print("-" * 50)
    print(f"[*] กำลังเคาะประตูบ้านเลขที่: {target_ip}")
    print(f"[*] เวลาเริ่ม: {datetime.now()}")
    print("-" * 50)

    try:
        # วนลูปเคาะทีละประตูตามลิสต์ข้างบน
        for port in COMMON_PORTS:
            # สร้างตัวเคาะประตู (Socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5) # รอแค่ 0.5 วิ ถ้าไม่ตอบถือว่าปิด
            
            # ลองเคาะ (Connect)
            result = sock.connect_ex((target_ip, port))
            
            if result == 0:
                # ถ้า connect ติด (return 0) แปลว่าเปิด!
                service_name = COMMON_PORTS[port]
                print(f"[+] เจอประตูเปิด!! -> Port {port}: {service_name}")
            else:
                # ถ้าอยากเห็นประตูที่ปิดด้วย ให้เอา comment บรรทัดล่างออก
                # print(f"[-] Port {port} ปิดอยู่")
                pass
                
            sock.close() # เคาะเสร็จต้องปิดตัวเคาะด้วย

    except KeyboardInterrupt:
        print("\n[!] ป๋ากดหยุดโปรแกรมทำไมครับ?")
    except socket.gaierror:
        print("\n[!] หา IP นี้ไม่เจอครับ")
    except socket.error:
        print("\n[!] เชื่อมต่อไม่ได้เลย Server ล่มหรือเปล่า?")

    print("-" * 50)
    print("[*] สแกนเสร็จเรียบร้อยครับป๋า!")

if __name__ == "__main__":
    # ให้ป๋ากรอก IP ที่เจอเมื่อกี้ (แนะนำ 10.1.102.6 ตัวที่น่าสงสัย)
    target = input("กรอก IP ที่ต้องการสแกน (เช่น 10.1.102.6): ")
    if target:
        scan_ports(target)
    else:
        print("ป๋าลืมใส่ IP ครับ!")