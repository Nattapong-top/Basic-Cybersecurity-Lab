import subprocess

def list_wifi_windows():
    # สั่ง cmd ให้รันคำสั่ง "netsh wlan show networks"
    # เป็นการยืมมือ Windows ให้สแกนให้
    result = subprocess.check_output(["netsh", "wlan", "show", "networks"], shell=True)
    
    # แปลงผลลัพธ์ที่ได้เป็นข้อความภาษาไทย/อังกฤษ (decode)
    # Windows ภาษาไทยอาจต้องใช้ cp874, อังกฤษใช้ utf-8 หรือ cp437
    try:
        decoded_result = result.decode('cp874') # ลอง cp874 สำหรับเครื่องไทย
    except:
        decoded_result = result.decode('utf-8', errors='ignore')

    print(decoded_result)

print("รายชื่อ Wi-Fi ที่ Windows มองเห็น:")
list_wifi_windows()