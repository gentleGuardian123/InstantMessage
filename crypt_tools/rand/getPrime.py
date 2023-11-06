
from crypt_tools.rand.fund import *

def getPrime(length=128):
    num = 0
    for _ in range(length):
        num = (num << 1) ^ randint(0, 1)
    while not is_prime(num):
        num += 1
    return num
