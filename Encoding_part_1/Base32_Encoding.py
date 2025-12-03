import base64

def base32ToString(b):
    return base64.b32decode(b).decode('utf-8')

def stringToBase32(s:str):
    return base64.b32encode(s.encode('utf-8'))

word = 'Hello World!'
encode = stringToBase32(word)
print(f'Encode Base32: {encode}')

decode = base32ToString(encode)
print(f'Decode Base32: {decode}')


code_ncsa = 'KRUGKIDGNRQWOIDJOMQGG4TZOB2G662CGMZF6YZQMQYW4Z27IIYWOXZQNZWHS7I='
decode_ncsa = base32ToString(code_ncsa)
print(f'Decode NCSA: {decode_ncsa}')
