a = '78 67 83 65 32 84 104 97 105 108 97 110 100'

def ascll_code(a:str):
    code = [chr(int(n)) for n in a.split()]
    return code

word_str = ascll_code(a)
print(''.join(word_str))
# NCSA Thailand

b = 'NCSA Thailand'

def hax_encode(b:str):
    code = [chr(n) for n in b]
    return code
word_to_hex = hax_encode(b)
print(word_to_hex)
