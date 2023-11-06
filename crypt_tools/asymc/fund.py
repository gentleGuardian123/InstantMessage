
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
        # import pdb; pdb.set_trace()
        s = r // rp
        r, a, b, rp, ap, bp = rp, ap, bp, r - s * rp, a - s * ap, b - s * bp
    return b % m

def get_sk(p, q, e):
    phi = (p - 1) * (q - 1)
    return get_inv(e, phi)

def CRT(c, m, n):
    res = 0
    N = 1
    for item in m:
        N *= item
    for i in range(n):
        temp = N // m[i]
        c[i] *= temp * get_inv(temp, m[i])
    for item in c:
        res = (res + item) % N
    return res


