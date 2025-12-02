import socket
import subprocess
import platform
import concurrent.futures
from datetime import datetime

# --- ตั้งค่าประตู (Port) ที่อยากสแกน ---
TARGET_PORTS = {
    21: "FTP",
    22: "SSH (Linux)",
    80: "HTTP (Web/Printer Config)",
    443: "HTTPS (Web Secure)",
    445: "SMB (Windows Share/File Server)",
    3389: "RDP (Remote Desktop)",
    9100: "Printer JetDirect (เครื่องปริ้นท์ชัวร์ๆ)"
}

def ping_host(ip):
    """ฟังก์ชันเช็กว่าเครื่องเปิดอยู่ไหม (Ping)"""
    param_n = '-n' if platform.system().lower() == 'windows' else '-c'
    param_w = '-w' if platform.system().lower() == 'windows' else '-W'
    command = ['ping', param_n, '1', param_w, '300', ip] # รอแค่ 300ms พอ เร็วดี
    
    try:
        response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if response == 0:
            return ip
    except:
        return None
    return None

def scan_ports_of_host(ip):
    """ฟังก์ชันเคาะประตู (Port Scan) สำหรับ 1 เครื่อง"""
    open_ports = []
    
    # ลองเคาะทีละประตู ตามรายการข้างบน
    for port in TARGET_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) # รอ 0.5 วิ
        
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(f"{port} ({TARGET_PORTS[port]})")
        sock.close()
    
    return ip, open_ports

def run_lan_scan(network_prefix):
    print(f"\n[*] 🚀 เริ่มภารกิจสแกนวง: {network_prefix}.1 - {network_prefix}.254")
    print(f"[*] กำลังกวาดหาเครื่องที่เปิดอยู่... (ใจเย็นๆ นะครับป๋า)")
    
    # 1. สร้างรายการ IP ทั้งหมด
    all_ips = [f"{network_prefix}.{i}" for i in range(1, 255)]
    live_hosts = []

    # 2. PING SWEEP (หาเครื่องเป็น)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(ping_host, all_ips)
        for ip in results:
            if ip:
                live_hosts.append(ip)

    print(f"\n[+] เจอเครื่องที่เปิดอยู่ทั้งหมด: {len(live_hosts)} เครื่อง")
    print("[*] กำลังเจาะดู Port ของแต่ละเครื่อง... (ขั้นตอนนี้อาจใช้เวลาแป๊บนึง)\n")

    # 3. PORT SCAN (เจาะดูไส้ใน)
    print("=" * 60)
    print(f"{'IP Address':<20} | {'Open Services'}")
    print("=" * 60)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # สั่งสแกนพอร์ตหลายๆ เครื่องพร้อมกัน
        results = executor.map(scan_ports_of_host, live_hosts)
        
        for ip, ports in results:
            if ports:
                # ถ้าเจอพอร์ตเปิด ให้โชว์ออกมา
                ports_str = ", ".join(ports)
                print(f"{ip:<20} | ✅ {ports_str}")
            else:
                # ถ้าไม่เจอพอร์ตเปิดเลย (แต่อยู่บ้าน)
                print(f"{ip:<20} | 🔒 (ปิดทุกพอร์ตที่สแกน)")

    print("=" * 60)
    print("[OK] ภารกิจเสร็จสิ้นครับป๋า! 😎")

if __name__ == "__main__":
    print("--- โปรแกรม Super LAN Scanner ฉบับป๋า ---")
    # รับค่า 3 ชุดแรก
    target_subnet = input("กรอก 3 ชุดแรกของ IP (เช่น 10.1.102): ").strip()
    
    if target_subnet:
        run_lan_scan(target_subnet)
    else:
        print("ป๋าลืมกรอก IP ครับ!")