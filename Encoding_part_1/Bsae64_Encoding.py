import base64

def stringToBase64(s:str):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b:str):
    return base64.b64decode(b).decode('utf-8')

word = 'Hello, world'
encode = stringToBase64(word)
print(encode)

decode = base64ToString(encode)
print(decode)

code_ncsa = 'VGhlIGZsYWcgaXMgY3J5cHRve3RoZV9lbmMwZDMxbmdfMXNfbjB0X1MzY3IzN30='
decode_ncsa = base64ToString(code_ncsa)
print(decode_ncsa)


'''
b'SGVsbG8sIHdvcmxk'
Hello, world
The flag is crypto{the_enc0d31ng_1s_n0t_S3cr37}
'''