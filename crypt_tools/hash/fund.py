# 算法中“字”定义为32位的比特串
MAX_32 = 0xffffffff

# 32位循环左移
def lshift(x: int, i: int) -> int:
    return ((x << (i % 32)) & MAX_32) + (x >> (32 - i % 32))

# 常量T，用于计算
def T(j) -> int:
    if 0 <= j <= 15:
        return 0x79cc4519
    return 0x7a879d8a

# 布尔函数FFj
def FF(j: int, x: int, y: int, z: int) -> int:
    if 0 <= j <= 15:
        return x ^ y ^ z
    return (x & y) | (x & z) | (y & z)

# 布尔函数GGj
def GG(j: int, x: int, y: int, z: int) -> int:
    if 0 <= j <= 15:
        return x ^ y ^ z
    return (x & y) | (~x & z)

# 置换函数P0
def P0(x: int) -> int:
    return x ^ lshift(x, 9) ^ lshift(x, 17)

# 置换函数P1
def P1(x: int) -> int:
    return x ^ lshift(x, 15) ^ lshift(x, 23)

# 消息填充函数，对长度为l(l < 2^64)比特的消息s，填充至长度为512比特的倍数
def fill(s: bytes) -> str:
    msg = ''.join([bin(b)[2:].zfill(8) for b in s])
    k = (960 - len(msg) - 1) % 512
    padded_msg = msg + '1' + '0'*k + bin(len(msg))[2:].zfill(64)
    return hex(int(padded_msg, 2))[2:].zfill(len(padded_msg) // 4)

