
from crypt_tools.asymc.fund import *
from crypt_tools.rand.getPrime import getPrime

class rsa:
    n, p, q = None, None,None
    e = 65535

    def __init__(self, length=2048):
        self.p, self.q = getPrime(length), getPrime(length)
        self.n = self.p * self.q

    def encrypt(self, msg, mode=0):
        if not mode:
            return qucpow(msg, self.e, self.n)
        else:
            invp = get_inv(self.e, self.p - 1)
            invq = get_inv(self.e, self.q - 1)
            c1 = qucpow(msg, invp, self.p)
            c2 = qucpow(msg, invq, self.q)
            return CRT([c1, c2], [self.p, self.q], 2)

