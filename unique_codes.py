from random import randint as r
token = ''
token_sym = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'


def unique_code():
    unique_code = ''
    for i in range(6):
        unique_code += str(r(0, 9))
    return unique_code


def token():
    token = ''
    for i in range(20):
        token += token_sym[r(0, len(token_sym) - 1)]
    return token
