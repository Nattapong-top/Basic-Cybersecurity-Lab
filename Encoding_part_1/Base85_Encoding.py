'''Base85 จะใช้เหมือนๆกับ Base64 
โดยมีการแทนค่าได้หลากหลายมากกว่าใน Base64 
ซึ่งถูกนำไปใช้ใน Adobe's PostScript และ PDF file formats.'''

import base64

def base85ToString(s:str):
    return base64.a85decode(s).decode('utf-8')

code = "<+ohcAo(mg+DGm>@rcj6FDlM&6q1N<F'iT:BJY&"

decode = base85ToString(code)
print(f'Decode: {decode}')