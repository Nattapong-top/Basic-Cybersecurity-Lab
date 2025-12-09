def encrypt_caesar(text:str, key:int):
    result = ''

    for char in text:
        if char.isalpha():
            # แปลงเป็น ascll
            # fixbug xyz ไม่วนกลับมา เป็น abc
            start_ascii = ord('a') if char.islower() else ord('A')

            # 1. แปลงตัวอักษรให้เป็นเลขลำดับ (0-25)
            # ตัวอย่าง: 'x' (120) - 'a' (97) = 23
            char_index = ord(char) - start_ascii

            # 2. เลื่อนค่าและใช้ modulo 26 เพื่อวนกลับไปเริ่มต้นใหม่
            # ตัวอย่าง: (23 + 3) % 26 = 26 % 26 = 0
            shifted_index = (char_index + key) % 26

            # แปลงกลับเป็น ascii และตัวอักษร
            # ตัวอย่าง: 0 + 'a' (97) 97. chr(97) = 'a'
            result += chr(shifted_index + start_ascii)
        else:
            # แปลงกลับเป็นตัวอักษร
            result += char
    return result

def decrypt_casar(cipher_text:str, key:int):
    # การถอดรหัสทำโดยใช้ key ตัวเดิม แต่สูตร Modulo เดียวกันเพื่อถอยค่า
    # (เราแค่เลื่อนค่าติดลบไป ซื่ง Modulo ใน Python จะจัดการให้วนกลับมาถูกฝั่ง)
    return encrypt_caesar(cipher_text, -key) # ใช้ key ติดลบเพื่อถอยหลัง

message = "xyz"
secret_key = 3  # กุญแจลับคือเลข 3

# 1. เข้ารหัส

encode_caesar = encrypt_caesar(message,secret_key)
print(encode_caesar)

decode_caesar = decrypt_casar(encode_caesar,secret_key)
print(decode_caesar)


        