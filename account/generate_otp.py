import random
import string

def generate_code_opt():
    rand = random.SystemRandom()
    code = rand.choices(string.digits, k=6)
    result = ''.join(code)
    return result
