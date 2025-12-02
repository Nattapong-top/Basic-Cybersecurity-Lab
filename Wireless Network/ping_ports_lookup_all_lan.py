import socket
import subprocess
import platform
import concurrent.futures
from datetime import datetime

# --- 1. CONFIGURATION (ตั้งค่า) ---
TARGET_PORTS = {
    21: "FTP", 22: "SSH", 80: "HTTP", 443: "HTTPS", 445: "SMB", 3389: "RDP", 9100: "Printer"
}
MAX_WORKERS = 50 

# --- 2. FUNCTION: PING SWEEP (หาเครื่องที่เปิดอยู่) ---
def ping_host(ip):
    """รัน Ping ด้วย subprocess เพื่อเช็กว่า IP ตอบกลับหรือไม่"""
    param_n = '-n' if platform.system().lower() == 'windows' else '-c'
    param_w = '-w' if platform.system().lower() == 'windows' else '-W'
    command = ['ping', param_n, '1', param_w, '300', ip]
    
    try:
        # Ping 1 ครั้ง, รอ 300ms, ซ่อน Output
        response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if response == 0:
            return ip
    except:
        return None
    return None

# --- 3. FUNCTION: PORT SCAN (เคาะประตู) ---
def scan_ports(ip):
    """สแกน Port ที่กำหนดไว้บน IP ที่เปิดอยู่"""
    open_ports = []
    for port in TARGET_PORTS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5) 
        
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(f"{port} ({TARGET_PORTS[port]})")
        sock.close()
    return open_ports

# --- 4. FUNCTION: HOSTNAME LOOKUP (จับชื่อเครื่อง) ---
def get_hostname(ip):
    """
    พยายามหาชื่อเครื่อง (Hostname) ผ่าน Reverse DNS
    (ถ้า DNS Server ใน Office ตั้งค่าไว้ จะได้ชื่อที่อ่านง่าย)
    """
    try:
        # Reverse DNS Lookup (หาชื่อจาก IP)
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except socket.error:
        # ถ้าหาชื่อไม่ได้ หรือ NBTSTAT ถูกบล็อก
        return "Unknown/N/A"
# *หมายเหตุ: สำหรับชื่อ NetBIOS (JTTH-HQ...) ต้องใช้ nbtstat -A แยก*

# --- 5. WORKER (รวมร่างทุกขั้นตอนสำหรับ 1 IP) ---
def process_host(ip):
    """ฟังก์ชันหลักที่รันในแต่ละ Thread"""
    # 1. Ping Check (ต้องเปิดอยู่ก่อน)
    if not ping_host(ip): 
        return None # ถ้า Ping ไม่เจอ ให้ข้ามไปเลย

    # 2. Port Scan
    open_ports = scan_ports(ip)

    # 3. Hostname/Info Lookup
    hostname = get_hostname(ip)
    
    # ถ้า Port 445 เปิด (Windows) ลองเอาชื่อ NetBIOS จาก nbtstat มาใช้แทน
    if '445 (SMB)' in open_ports and hostname == "Unknown/N/A":
        # ถ้าอยากได้ชื่อ NetBIOS (JTTH-HQ...) ต้องเขียนโค้ดเรียก subprocess.run(['nbtstat', '-A', ip]) 
        # และจัดการ Parse ข้อมูลที่ซับซ้อนกว่านี้
        # ในที่นี้ให้ Paa รัน nbtstat ด้วยตัวเองสำหรับเครื่องที่น่าสงสัยแทนครับ (เช่น 10.1.102.29)
        pass 

    return {
        'ip': ip,
        'hostname': hostname,
        'ports': open_ports
    }

# --- 6. MAIN EXECUTION ---
if __name__ == "__main__":
    print("--- 🛠️ IT ASSET SCANNER (BY P'NATT) ---")
    
    target_subnet = input("กรอก 3 ชุดแรกของ IP ที่ต้องการสแกน (เช่น 10.1.102): ").strip()
    
    if not target_subnet:
        print("ป๋าลืมกรอก IP ครับ!")
        exit()

    start_time = datetime.now()
    all_ips = [f"{target_subnet}.{i}" for i in range(1, 255)]
    results_list = []
    
    print(f"[*] เริ่มสแกน {len(all_ips)} IPs ในวง {target_subnet}.x")
    
    # ใช้วิธี Multi-threading เพื่อรันทุกอย่างพร้อมกัน
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # สั่งให้ process_host ทำงานกับทุก IP ใน all_ips
        futures = executor.map(process_host, all_ips)
        
        # เก็บผลลัพธ์ที่สมบูรณ์
        for result in futures:
            if result:
                results_list.append(result)

    end_time = datetime.now()
    
    # --- 7. FINAL REPORT ---
    print("\n" + "=" * 80)
    print(f"{'Final Asset Scan Report':<79}")
    print(f"สแกนเสร็จสิ้น | เวลา: {(end_time - start_time).total_seconds():.2f} วินาที | พบ {len(results_list)} รายการ")
    print("=" * 80)
    
    print(f"{'IP Address':<18} | {'Hostname/DNS Name':<30} | {'Open Services'}")
    print("-" * 80)

    for item in sorted(results_list, key=lambda x: x['ip']):
        ports_str = ", ".join(item['ports']) if item['ports'] else "🔒 (ปิดทุกพอร์ตที่สแกน)"
        
        # สำหรับเครื่องที่ป๋าเคยเจอ: ลองเช็กชื่อที่ได้
        hostname_display = item['hostname']
        if item['ip'] == '10.1.102.29':
             hostname_display = "JTTH-HQ... (Printer?)" # ใช้ชื่อที่เคยเจอมาใส่เป็น Notes
        
        print(f"{item['ip']:<18} | {hostname_display:<30} | {ports_str}")
        
    print("-" * 80)