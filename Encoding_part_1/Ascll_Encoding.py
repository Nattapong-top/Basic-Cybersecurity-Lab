a = '78 67 83 65 32 84 104 97 105 108 97 110 100'

def ascll_code(a:str):
    code = [chr(int(n)) for n in a.split()]
    return code

word_str = ascll_code(a)
print(''.join(word_str))
# NCSA Thailand