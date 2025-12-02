import subprocess
import platform
import concurrent.futures
import time

def ping_ip(ip):
    """
    ฟังก์ชันสำหรับ Ping 1 ครั้ง
    ถ้าเจอเครื่องตอบกลับ จะคืนค่า IP นั้นออกมา
    """
    # ตรวจสอบว่าเป็น Windows หรือ Linux/Mac เพื่อใช้คำสั่งให้ถูก
    param_n = '-n' if platform.system().lower() == 'windows' else '-c'
    param_w = '-w' if platform.system().lower() == 'windows' else '-W'
    
    # คำสั่ง ping: ส่ง 1 แพ็กเก็ต, รอแค่ 500ms (จะได้ไม่ต้องรอพวกที่ไม่ตอบนานๆ)
    command = ['ping', param_n, '1', param_w, '500', ip]
    
    # รันคำสั่งแบบเงียบๆ ไม่ต้องโชว์ข้อความรกรุงรัง
    response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if response == 0:
        return ip  # เจอเครื่อง! (Ping สำเร็จ)
    else:
        return None # ไม่เจอ

def run_scanner(network_prefix):
    print(f"\n[*] กำลังปูพรมสแกนวง: {network_prefix}.1 - {network_prefix}.254")
    print("[*] เครื่องป๋ากำลังทำงานหนักนิดนึงนะครับ...")
    
    # สร้างรายการ IP ทั้งหมดที่จะสแกน (1-254)
    ip_list = [f"{network_prefix}.{i}" for i in range(1, 255)]
    
    found_devices = []
    
    # ใช้ ThreadPoolExecutor เพื่อยิง Ping พร้อมกัน 50 เส้น (เร็วมาก!)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # สั่งให้ทำงานและเก็บผลลัพธ์
        results = executor.map(ping_ip, ip_list)
        
        for result in results:
            if result:
                found_devices.append(result)
                # print(f"  -> เจอแล้ว! {result}") # เอาคอมเมนต์ออกถ้าอยากเห็นเด้งทีละตัว
                
    return found_devices

if __name__ == "__main__":
    print("--- โปรแกรม Ping Sweep ฉบับป๋า ---")
    
    # 1. ให้ป๋ากรอกเลขหน้าของวงแลนที่อยากสแกน
    # ตัวอย่าง: ถ้า Printer อยู่ IP 192.168.50.55 ให้กรอก "192.168.50"
    target_subnet = input("กรอก 3 ชุดแรกของ IP ที่ต้องการสแกน (เช่น 192.168.1): ").strip()
    
    if target_subnet:
        start_time = time.time()
        
        # เริ่มสแกน
        active_hosts = run_scanner(target_subnet)
        
        # สรุปผล
        print("\n" + "="*40)
        print(f"สรุปผลการสแกนวง {target_subnet}.x")
        print("="*40)
        
        if active_hosts:
            for host in active_hosts:
                print(f"[+] เจอเครื่องที่ IP: {host}")
            print(f"\nรวมทั้งหมด: {len(active_hosts)} เครื่อง")
        else:
            print("[-] เงียบกริบ... ไม่เจอใครตอบกลับเลยครับ")
            
        print(f"ใช้เวลาไป: {time.time() - start_time:.2f} วินาที")
    else:
        print("ป๋าลืมกรอก IP ครับ ลองใหม่นะ")