import subprocess
import re

def scan_wifi_security():
    print("กำลังสแกนหาเครือข่าย Wi-Fi... (อาจใช้เวลาสักครู่)")
    print("-" * 60)
    print(f"{'SSID (ชื่อ Wifi)':<30} | {'Security Type (ระบบความปลอดภัย)'}")
    print("-" * 60)

    try:
        # ใช้ subprocess เพื่อสั่งคำสั่ง 'nmcli' ของ Linux (Network Manager CLI)
        # คำสั่งจริงคือ: nmcli -f SSID,SECURITY dev wifi
        cmd_output = subprocess.check_output(
            ["nmcli", "-f", "SSID,SECURITY", "dev", "wifi"], 
            stderr=subprocess.STDOUT
        )
        
        # แปลงข้อมูลจาก bytes เป็น string
        output_str = cmd_output.decode("utf-8")
        
        # แยกบรรทัดเพื่อมาตรวจสอบทีละบรรทัด
        lines = output_str.split('\n')

        # วนลูปตรวจสอบข้อมูล (ข้ามบรรทัดแรกที่เป็นหัวตาราง)
        for line in lines[1:]:
            if not line.strip():
                continue # ข้ามบรรทัดว่าง
            
            # ข้อมูลจะมาในรูปแบบ "ชื่อWifi      ประเภทความปลอดภัย"
            # เราจะแยกมันออกจากกัน (nmcli เว้นวรรคค่อนข้างกว้าง)
            parts = re.split(r'\s{2,}', line.strip())
            
            if len(parts) >= 2:
                ssid = parts[0]
                security = parts[1]
                
                # ตกแต่งการแสดงผล
                display_sec = security
                
                # ถ้าเจอ WPA3 (SAE) ให้ใส่ดาว ★ แจ้งเตือนว่าปลอดภัยสูง
                if "SAE" in security or "WPA3" in security:
                    display_sec = f"★ {security} (WPA3 - Secure!)"
                # ถ้าเจอ WEP ให้แจ้งเตือนว่าอันตราย
                elif "WEP" in security:
                    display_sec = f"⚠️ {security} (WEP - DANGEROUS!)"
                
                print(f"{ssid:<30} | {display_sec}")

    except FileNotFoundError:
        print("Error: ไม่พบคำสั่ง nmcli (รันใน Kali Linux หรือยังครับ?)")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    scan_wifi_security()