'''Base62 นั้นจะคล้ายกับ Base32, Base64
แต่ตัดส่วนอักขระ (symbol) บางส่วนทิ้งในระบบที่ไม่
อนุญาตหรือไม่เข้าใจ 
โดยทำให้คนและการประมวลผลทำได้ง่ายมากขึ้น

pip install pybase62
'''

import base62

def base62ToString(b):
    return base62.decodebytes(b).decode('utf-8')

ciphertext = '1Ke0zSzxd539Z1cYhF4ILB80p5XGj0J0MhNrA1zo07UVx'

decode = base62ToString(ciphertext)
print(f'Decode: {decode}')