import scapy.all as scapy
import socket

# ฟังก์ชันสำหรับหา IP ของเครื่องตัวเองและ Subnet (เช่น 192.168.1.1/24)
def get_own_ip_range():
    # หา IP เครื่องตัวเองก่อน
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"[*] เครื่องของป๋า IP คือ: {local_ip}")
    
    # ตัดเอาแค่ 3 ชุดแรก แล้วเติม .1/24 เพื่อสแกนทั้งวง
    # เช่น ถ้า IP 192.168.1.45 -> จะได้ 192.168.1.1/24
    ip_parts = local_ip.split('.')
    network_range = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.1/24"
    return network_range

def scan(ip):
    print(f"\n[*] กำลังเริ่มสแกนหาคนในวง Wi-Fi: {ip}")
    print("[*] รอสักครู่นะครับป๋า...\n")
    
    # 1. สร้างแพ็กเก็ต ARP Request (ถามหาเจ้าของ IP)
    arp_request = scapy.ARP(pdst=ip)
    
    # 2. สร้างกรอบ Ethernet เพื่อส่งไปหาทุกคน (Broadcast ff:ff:ff:ff:ff:ff)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    
    # 3. รวมร่างแพ็กเก็ต
    arp_request_broadcast = broadcast/arp_request
    
    # 4. ส่งออกไปและรอรับคำตอบ (timeout=1 คือรอ 1 วินาที)
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("----------------------------------------------------")
    print("IP Address\t\tMAC Address")
    print("----------------------------------------------------")
    for client in results_list:
        print(f"{client['ip']}\t\t{client['mac']}")
    print(f"\n[OK] เจอทั้งหมด {len(results_list)} อุปกรณ์ครับ")

# --- เริ่มทำงาน ---
if __name__ == "__main__":
    try:
        # หา Network Range อัตโนมัติ
        target_ip = get_own_ip_range()
        # เริ่มสแกน
        scan_result = scan(target_ip)
        # แสดงผล
        print_result(scan_result)
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        print("คำแนะนำ: อย่าลืมลง Npcap และรันโปรแกรมด้วยสิทธิ์ Administrator นะครับ")