import string
from random import choice


chars = string.ascii_letters
specials = string.punctuation
digits = string.digits

def gen_password(len: int = 8, *, digits=digits, specials=specials)-> str: 
    password: str = ""

    if digits is not None: 
        chars + digits
    
    if specials is not None: 
        chars + specials

    for _ in range(len): 
        password += choice(chars)
    return password


print(gen_password(16, specials=None))