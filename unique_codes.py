from random import randint as r
unique_code = ''
token = ''
token_sym = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*_1234567890'
for i in range(6):
    unique_code += str(r(0, 9))
for i in range(20):
    token += token_sym[r(0, len(token_sym))]
