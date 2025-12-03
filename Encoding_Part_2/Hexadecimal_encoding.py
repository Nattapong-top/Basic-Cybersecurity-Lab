'''Hexadecimal คือจะเป็นลักษณะของการใช้งานในรูปแบบของ
เลขฐาน 16 โดยขั้นตอนการแปลงระหว่าง Character ให้ไปเป็น Hex นั้นจะมีขั้นตอนเป็น

เปลี่ยนจาก Character ให้กลายเป็น Decimal (ASCII)
Decimal แปลงเป็น Hexadecimal ได้'''

import codecs

word = 'SEC Playground'
enstring = word.encode('utf-8').hex()
print('Hex:', enstring)

destring = codecs.decode(enstring, 'hex').decode('utf-8')
print('String: ', destring)

code_hex = '54 68 65 20 66 6c 61 67 20 69 73 20 63 72 79 70 74 6f 7b 68 33 78 5f 33 6e 63 30 64 31 6e 67 7d'

now_hex = ''.join(code_hex.split())
decode = codecs.decode(now_hex, 'hex').decode('utf-8')
print(f'Decode: ', decode)