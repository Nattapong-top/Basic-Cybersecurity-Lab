# ป๋าต้องลง library ก่อนนะ: pip install cryptography
from cryptography.fernet import Fernet

# 1. สร้างกุญแจ (Key) ขึ้นมา (เปรียบเหมือนปั๊มลูกกุญแจ)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

print(f"กุญแจลับของป๋า: {key}")

# 2. ข้อความที่ต้องการส่ง (Data)
message = "เงินเดือนป๋า 53,000 บาท".encode() # ต้องแปลงเป็น bytes ก่อน

# 3. ทำการเข้ารหัส (Encrypt) - จะได้ขยะอ่านไม่ออก
cipher_text = cipher_suite.encrypt(message)
print(f"ข้อความที่ถูกเข้ารหัส: {cipher_text}")

# 4. ทำการถอดรหัส (Decrypt) - โดยใช้กุญแจเดิม
plain_text = cipher_suite.decrypt(cipher_text)
print(f"ข้อความที่ถอดออกมา: {plain_text.decode()}")