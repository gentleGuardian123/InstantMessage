from crypt_tools.rand.getRandom import getRandom

def plus(X, Z):  # GF(256)加法
    x = int('0x'+X, 16)
    z = int('0x'+Z, 16)
    return '{:02x}'.format(x^z)

def time(X, Z):  # GF(256)乘法
    x = int('0x'+X, 16)
    z = int('0x'+Z, 16)
    ans = 0
    while z > 0:
        if z & 1:
            ans ^= x
        x <<= 1
        if x & 256 == 256:
            x ^= 283
        x &= 255
        z >>= 1
    return '{:02x}'.format(ans)

def qpow(b, n):  # GF(256)快速模幂
    res = '01'  # 调整初值
    while n:
        if (n&1) == 1:
            res = time(res, b)
        n >>= 1
        b = time(b, b)
    return res

def inv(x):  # GF(256)求逆元
    return qpow(x, 254)

def xor(a, b):  # 任意长二进制字符串的异或 (2进制不含前缀输入，2进制不含前缀输出)
    wid = len(a)
    return bin(int('0b'+a, 2) ^ int('0b'+b, 2))[2:].zfill(wid)

def s_trans(b, s):  # S盒变换或逆变换，输入1个字节，输出1个字节 (16进制不含前缀输入，16进制不含前缀输出)
    return s[int('0x'+b[0], 16)][int('0x'+b[1], 16)][2:]

def key_ext(k, s, l):  # 密钥扩展，输入192/256位密钥，输出52/60个32位的子密钥的列表 (16进制含前缀输入，2进制不含前缀输出)
    rcon = [
        '0x01000000', '0x02000000', '0x04000000', '0x08000000', '0x10000000',
        '0x20000000', '0x40000000', '0x80000000', '0x1b000000', '0x36000000',
        '0x6c000000', '0xd8000000', '0xab000000', '0x4d000000', '0x9a000000',
        '0x2f000000'
    ]
    if l == "L-128":
        k = bin(int(k, 16))[2:].zfill(128)
        w0, w1, w2, w3 = k[0:32], k[32:64], k[64:96], k[96:128]
        res = [w0 + w1 + w2 + w3]
        for i in range(10):
            t0 = w3[8:32] + w3[0:8]  # 字循环
            t0 = (s_trans('{:02x}'.format(int('0b' + t0[0:8], 2)), s)
                  + s_trans('{:02x}'.format(int('0b' + t0[8:16], 2)), s)
                  + s_trans('{:02x}'.format(int('0b' + t0[16:24], 2)), s)
                  + s_trans('{:02x}'.format(int('0b' + t0[24:32], 2)), s))  # 字节代换
            t0 = xor(bin(int('0x' + t0, 16))[2:].zfill(32), bin(int(rcon[i], 16))[2:].zfill(32))  # 与轮常量异或
            t0 = xor(t0, w0)
            t1 = xor(t0, w1)
            t2 = xor(t1, w2)
            t3 = xor(t2, w3)
            w0, w1, w2, w3 = t0, t1, t2, t3
            res.extend([w0 + w1 + w2 + w3])
        return res
    elif l == "L-192":
        k = bin(int(k, 16))[2:].zfill(192)
        w0, w1, w2, w3, w4, w5 = k[0:32], k[32:64], k[64:96], k[96:128], k[128:160], k[160:192]
        res = [w0, w1, w2, w3, w4, w5]
        for i in range(10):
            t0 = w5[8:32] + w5[0:8]  # 字循环
            t0 = (s_trans('{:02x}'.format(int('0b'+t0[0:8], 2)), s)
                  + s_trans('{:02x}'.format(int('0b'+t0[8:16], 2)), s)
                  + s_trans('{:02x}'.format(int('0b'+t0[16:24], 2)), s)
                  + s_trans('{:02x}'.format(int('0b'+t0[24:32], 2)), s))  # 字节代换
            t0 = xor(bin(int('0x'+t0, 16))[2:].zfill(32), bin(int(rcon[i], 16))[2:].zfill(32))  # 与轮常量异或
            t0 = xor(t0, w0)
            t1 = xor(t0, w1)
            t2 = xor(t1, w2)
            t3 = xor(t2, w3)
            t4 = xor(t3, w4)
            t5 = xor(t4, w5)
            w0, w1, w2, w3, w4, w5 = t0, t1, t2, t3, t4, t5
            res.extend([w0, w1, w2, w3, w4, w5])
    else:
        k = bin(int(k, 16))[2:].zfill(256)
        w0, w1, w2, w3 = k[0:32], k[32:64], k[64:96], k[96:128]
        w4, w5, w6, w7 = k[128:160], k[160:192], k[192:224], k[224:256]
        res = [w0, w1, w2, w3, w4, w5, w6, w7]
        for i in range(10):
            t0 = w7[8:32] + w7[0:8]  # 字循环
            t0 = (s_trans('{:02x}'.format(int('0b' + t0[0:8], 2)), s)
                  + s_trans('{:02x}'.format(int('0b' + t0[8:16], 2)), s)
                  + s_trans('{:02x}'.format(int('0b' + t0[16:24], 2)), s)
                  + s_trans('{:02x}'.format(int('0b' + t0[24:32], 2)), s))  # 字节代换
            t0 = xor(bin(int('0x' + t0, 16))[2:].zfill(32), bin(int(rcon[i], 16))[2:].zfill(32))  # 与轮常量异或
            t0 = xor(t0, w0)
            t1 = xor(t0, w1)
            t2 = xor(t1, w2)
            t3 = xor(t2, w3)
            t4 = (s_trans('{:02x}'.format(int('0b' + t3[0:8], 2)), s)
                  + s_trans('{:02x}'.format(int('0b' + t3[8:16], 2)), s)
                  + s_trans('{:02x}'.format(int('0b' + t3[16:24], 2)), s)
                  + s_trans('{:02x}'.format(int('0b' + t3[24:32], 2)), s))  # 字节代换
            t4 = xor(bin(int('0x' + t4, 16))[2:].zfill(32), w4)
            t5 = xor(t4, w5)
            t6 = xor(t5, w6)
            t7 = xor(t6, w7)
            w0, w1, w2, w3, w4, w5, w6, w7 = t0, t1, t2, t3, t4, t5, t6, t7
            res.extend([w0, w1, w2, w3, w4, w5, w6, w7])
    m = 11 if l == "L-128" else (13 if l == "L-192" else 15)
    res = [res[i*4] + res[i*4+1] + res[i*4+2] + res[i*4+3] for i in range(m)]
    return res

def byt_sub(s, box):  # 字节替换，128位无前缀2进制输入，128位无前缀2进制输出；f=0为逆行移位
    res = ''
    for i in range(16):
        res += bin(int(s_trans('{:02x}'.format(int('0b'+s[8*i:8*(i+1)],2)), box), 16))[2:].zfill(8)
    return res

def shf_row(s, f):  # 行移位，128位无前缀2进制输入，128位无前缀2进制输出；f=0为逆行移位
    if f:
        return (s[0:8] + s[40:48] + s[80:88] + s[120:128]
                + s[32:40] + s[72:80] + s[112:120] + s[24:32]
                + s[64:72] + s[104:112] + s[16:24] + s[56:64]
                + s[96:104] + s[8:16] + s[48:56] + s[88:96])
    return (s[0:8] + s[104:112] + s[80:88] + s[56:64]
            + s[32:40] + s[8:16] + s[112:120] + s[88:96]
            + s[64:72] + s[40:48] + s[16:24] + s[120:128]
            + s[96:104] + s[72:80] + s[48:56] + s[24:32])

def mix_col(s, f):  # 列混淆，128位无前缀2进制输入，128位无前缀2进制输出；f=0为逆列混淆
    res = [['00']*4 for _ in range(4)]
    m = [
        ['02', '03', '01', '01'],
        ['01', '02', '03', '01'],
        ['01', '01', '02', '03'],
        ['03', '01', '01', '02']
    ]
    if not f:
        m = [
            ['0e', '0b', '0d', '09'],
            ['09', '0e', '0b', '0d'],
            ['0d', '09', '0e', '0b'],
            ['0b', '0d', '09', '0e']
        ]
    ms = [['{:02x}'.format(int('0b'+s[32*j+8*i:32*j+8*(i+1)], 2)) for j in range(4)] for i in range(4)]
    for j in range(4):
        for i in range(4):
            for k in range(4):
                res[j][i] = plus(res[j][i], time(m[i][k], ms[k][j]))
    return bin(int('0x'+''.join([''.join(r) for r in res]), 16))[2:].zfill(128)

# AES，32位有前缀16进制输入，128位无前缀2进制子密钥列表输入，f=0为解密，共进行10轮；32位有前缀16进制输出
def roud_fuc(k_lst, s, mode):
    s = bin(int(s, 16))[2:].zfill(128)
    if mode == 0:
        s = xor(s, k_lst[0])  # 初始轮密钥加
        for i in range(9):
            s = xor(mix_col(shf_row(byt_sub(s, BOX[mode]), True), True), k_lst[i+1])
        s = xor(shf_row(byt_sub(s, box), True), k_lst[10])
    else:
        k_lst = k_lst[::-1]
        s = xor(s, k_lst[0])  # 初始轮密钥加
        for i in range(9):
            s = mix_col(xor(byt_sub((shf_row(s, False)), box), k_lst[i+1]), False)
        s = xor(byt_sub((shf_row(s, False)), box), k_lst[10])
    return '0x{:032x}'.format(int('0b'+s, 2))

def key_generate(length):
    if length == "L-128":
        return getRandom(128)
    elif length == "L-192":
        return getRandom(192)
    elif length == "L-256":
        return getRandom(256)

box = [
    ['0x63', '0x7c', '0x77', '0x7b', '0xf2', '0x6b', '0x6f', '0xc5', '0x30', '0x01', '0x67', '0x2b', '0xfe', '0xd7', '0xab', '0x76'],
    ['0xca', '0x82', '0xc9', '0x7d', '0xfa', '0x59', '0x47', '0xf0', '0xad', '0xd4', '0xa2', '0xaf', '0x9c', '0xa4', '0x72', '0xc0'],
    ['0xb7', '0xfd', '0x93', '0x26', '0x36', '0x3f', '0xf7', '0xcc', '0x34', '0xa5', '0xe5', '0xf1', '0x71', '0xd8', '0x31', '0x15'],
    ['0x04', '0xc7', '0x23', '0xc3', '0x18', '0x96', '0x05', '0x9a', '0x07', '0x12', '0x80', '0xe2', '0xeb', '0x27', '0xb2', '0x75'],
    ['0x09', '0x83', '0x2c', '0x1a', '0x1b', '0x6e', '0x5a', '0xa0', '0x52', '0x3b', '0xd6', '0xb3', '0x29', '0xe3', '0x2f', '0x84'],
    ['0x53', '0xd1', '0x00', '0xed', '0x20', '0xfc', '0xb1', '0x5b', '0x6a', '0xcb', '0xbe', '0x39', '0x4a', '0x4c', '0x58', '0xcf'],
    ['0xd0', '0xef', '0xaa', '0xfb', '0x43', '0x4d', '0x33', '0x85', '0x45', '0xf9', '0x02', '0x7f', '0x50', '0x3c', '0x9f', '0xa8'],
    ['0x51', '0xa3', '0x40', '0x8f', '0x92', '0x9d', '0x38', '0xf5', '0xbc', '0xb6', '0xda', '0x21', '0x10', '0xff', '0xf3', '0xd2'],
    ['0xcd', '0x0c', '0x13', '0xec', '0x5f', '0x97', '0x44', '0x17', '0xc4', '0xa7', '0x7e', '0x3d', '0x64', '0x5d', '0x19', '0x73'],
    ['0x60', '0x81', '0x4f', '0xdc', '0x22', '0x2a', '0x90', '0x88', '0x46', '0xee', '0xb8', '0x14', '0xde', '0x5e', '0x0b', '0xdb'],
    ['0xe0', '0x32', '0x3a', '0x0a', '0x49', '0x06', '0x24', '0x5c', '0xc2', '0xd3', '0xac', '0x62', '0x91', '0x95', '0xe4', '0x79'],
    ['0xe7', '0xc8', '0x37', '0x6d', '0x8d', '0xd5', '0x4e', '0xa9', '0x6c', '0x56', '0xf4', '0xea', '0x65', '0x7a', '0xae', '0x08'],
    ['0xba', '0x78', '0x25', '0x2e', '0x1c', '0xa6', '0xb4', '0xc6', '0xe8', '0xdd', '0x74', '0x1f', '0x4b', '0xbd', '0x8b', '0x8a'],
    ['0x70', '0x3e', '0xb5', '0x66', '0x48', '0x03', '0xf6', '0x0e', '0x61', '0x35', '0x57', '0xb9', '0x86', '0xc1', '0x1d', '0x9e'],
    ['0xe1', '0xf8', '0x98', '0x11', '0x69', '0xd9', '0x8e', '0x94', '0x9b', '0x1e', '0x87', '0xe9', '0xce', '0x55', '0x28', '0xdf'],
    ['0x8c', '0xa1', '0x89', '0x0d', '0xbf', '0xe6', '0x42', '0x68', '0x41', '0x99', '0x2d', '0x0f', '0xb0', '0x54', '0xbb', '0x16']
]

inv_box = [
    ['0x52', '0x09', '0x6a', '0xd5', '0x30', '0x36', '0xa5', '0x38', '0xbf', '0x40', '0xa3', '0x9e', '0x81', '0xf3', '0xd7', '0xfb'],
    ['0x7c', '0xe3', '0x39', '0x82', '0x9b', '0x2f', '0xff', '0x87', '0x34', '0x8e', '0x43', '0x44', '0xc4', '0xde', '0xe9', '0xcb'],
    ['0x54', '0x7b', '0x94', '0x32', '0xa6', '0xc2', '0x23', '0x3d', '0xee', '0x4c', '0x95', '0x0b', '0x42', '0xfa', '0xc3', '0x4e'],
    ['0x08', '0x2e', '0xa1', '0x66', '0x28', '0xd9', '0x24', '0xb2', '0x76', '0x5b', '0xa2', '0x49', '0x6d', '0x8b', '0xd1', '0x25'],
    ['0x72', '0xf8', '0xf6', '0x64', '0x86', '0x68', '0x98', '0x16', '0xd4', '0xa4', '0x5c', '0xcc', '0x5d', '0x65', '0xb6', '0x92'],
    ['0x6c', '0x70', '0x48', '0x50', '0xfd', '0xed', '0xb9', '0xda', '0x5e', '0x15', '0x46', '0x57', '0xa7', '0x8d', '0x9d', '0x84'],
    ['0x90', '0xd8', '0xab', '0x00', '0x8c', '0xbc', '0xd3', '0x0a', '0xf7', '0xe4', '0x58', '0x05', '0xb8', '0xb3', '0x45', '0x06'],
    ['0xd0', '0x2c', '0x1e', '0x8f', '0xca', '0x3f', '0x0f', '0x02', '0xc1', '0xaf', '0xbd', '0x03', '0x01', '0x13', '0x8a', '0x6b'],
    ['0x3a', '0x91', '0x11', '0x41', '0x4f', '0x67', '0xdc', '0xea', '0x97', '0xf2', '0xcf', '0xce', '0xf0', '0xb4', '0xe6', '0x73'],
    ['0x96', '0xac', '0x74', '0x22', '0xe7', '0xad', '0x35', '0x85', '0xe2', '0xf9', '0x37', '0xe8', '0x1c', '0x75', '0xdf', '0x6e'],
    ['0x47', '0xf1', '0x1a', '0x71', '0x1d', '0x29', '0xc5', '0x89', '0x6f', '0xb7', '0x62', '0x0e', '0xaa', '0x18', '0xbe', '0x1b'],
    ['0xfc', '0x56', '0x3e', '0x4b', '0xc6', '0xd2', '0x79', '0x20', '0x9a', '0xdb', '0xc0', '0xfe', '0x78', '0xcd', '0x5a', '0xf4'],
    ['0x1f', '0xdd', '0xa8', '0x33', '0x88', '0x07', '0xc7', '0x31', '0xb1', '0x12', '0x10', '0x59', '0x27', '0x80', '0xec', '0x5f'],
    ['0x60', '0x51', '0x7f', '0xa9', '0x19', '0xb5', '0x4a', '0x0d', '0x2d', '0xe5', '0x7a', '0x9f', '0x93', '0xc9', '0x9c', '0xef'],
    ['0xa0', '0xe0', '0x3b', '0x4d', '0xae', '0x2a', '0xf5', '0xb0', '0xc8', '0xeb', '0xbb', '0x3c', '0x83', '0x53', '0x99', '0x61'],
    ['0x17', '0x2b', '0x04', '0x7e', '0xba', '0x77', '0xd6', '0x26', '0xe1', '0x69', '0x14', '0x63', '0x55', '0x21', '0x0c', '0x7d']
]

BOX = [box, inv_box]
