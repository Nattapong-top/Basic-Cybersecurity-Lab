'''Base58 นั้นจะคล้ายกับ Base32, Base64 
คือเป็นเครื่องหมายที่ใช้แทนระบบตัวเลขหรือเสียงในกาแปลงเพื่อ
ส่งค่าข้อมูล ซึ่งแตกต่างกับ Base64 
เนื่องด้วยมีการตัดส่วนท่ีอาจทำให้เข้าใจผิดได้ง่ายอย่าง 
(เช่น l, I, 0 และ O) เพื่อให้อ่านง่ายขึ้น โดยปกติ Base58 
มักถูกใช้ใน cryptocurrencies ต่างๆ เช่น Bitcoin, Ripple เป็นต้น'''

import base58

def base58ToString(b:str):
    return base58.b58decode(b).decode('utf-8')

b = 'DiMDr7jNvUnwKu3ZYQMuf897drn2DYFNrWDjcjsmx2LfnPpDFuodaw239au3dAt'

decode = base58ToString(b)
print(decode)