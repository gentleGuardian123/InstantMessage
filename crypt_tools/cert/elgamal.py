
from crypt_tools.hash.sm3 import sm3
from crypt_tools.rand.getRandom import getRandom
from crypt_tools.rand.getPrime import getPrime
from crypt_tools.cert.fund import *

class elgamal:
    p, g = None, None
    x, y = None, None

    def __init__(self, length=256):
        self.p = getPrime(length)
        self.g = get_root(self.p)
        self.x = getRandom(1024) % (self.p-1)
        while self.x <= 1:
            self.x = getRandom(1024) % (self.p - 1)
        self.y = qucpow(self.g, self.x, self.p)

    def sign(self, msg):  # 签名
        k = getRandom(256)
        M = sm3(msg)
        S1 = qucpow(self.g, k, self.p)
        S2 = get_inv(k, self.p - 1) * (M - self.x * S1) % (self.p - 1)
        return [S1, S2]

    def verify(self, msg, Sig):  # 验签
        M = sm3(msg)
        V1 = qucpow(self.g, M, self.p)
        V2 = qucpow(self.y, Sig[0], self.p) * qucpow(Sig[0], Sig[1], self.p) % self.p
        return V1 == V2




