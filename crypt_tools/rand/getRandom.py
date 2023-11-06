
from crypt_tools.rand.getPrime import getPrime

def BBS(l, p, q, s):
    res = 0
    n = p * q
    X = (s * s) % n
    for i in range(l):
        X = (X * X) % n
        res ^= ((X % 2) << i)
    return hex(res)

def getRandom(length=1024, seed=1152921504606846975):
    p, q = getPrime(), getPrime()
    return BBS(length, p, q, seed)
