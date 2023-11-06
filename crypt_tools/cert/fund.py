
def qucpow(m, e, n):  # m ** e % n
    res = 1
    prod = m
    while e != 0:
        if e & 1 == 1:
            res = (res * prod) % n
        prod = (prod * prod) % n
        e >>= 1
    return res

def get_inv(e, m):
    r, a, b = m, 1, 0
    rp, ap, bp = e, 0, 1
    while rp != 0:
        s = r // rp
        r, a, b, rp, ap, bp = rp, ap, bp, r - s * rp, a - s * ap, b - s * bp
    return b % m

def get_root(p):
    for i in range(2, p):
        if qucpow(i, (p-1)/2, p) == 1:
            return i
