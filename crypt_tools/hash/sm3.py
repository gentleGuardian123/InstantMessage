
from crypt_tools.hash.fund import *

def sm3(s: str) -> int:
    # 初始值，用于确定压缩函数寄存器的状态
    V = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e

    m = fill(s.encode())

    # 迭代过程
    for i in range(len(m) // 128):

        # 消息扩展
        Bi = m[i * 128: (i + 1) * 128]
        W = []
        for j in range(16):
            W.append(int(Bi[j * 8: (j + 1) * 8], 16))

        for j in range(16, 68):
            W.append(P1(W[j - 16] ^ W[j - 9] ^ lshift(W[j - 3], 15)) ^ lshift(W[j - 13], 7) ^ W[j - 6])
        W_ = []
        for j in range(64):
            W_.append(W[j] ^ W[j + 4])

        A, B, C, D, E, F, G, H = [V >> ((7 - i) * 32) & MAX_32 for i in range(8)]

        # 迭代计算
        for j in range(64):
            ss1 = lshift((lshift(A, 12) + E + lshift(T(j), j)) & MAX_32, 7)
            ss2 = ss1 ^ lshift(A, 12)
            tt1 = (FF(j, A, B, C) + D + ss2 + W_[j]) & MAX_32
            tt2 = (GG(j, E, F, G) + H + ss1 + W[j]) & MAX_32
            D = C
            C = lshift(B, 9)
            B = A
            A = tt1
            H = G
            G = lshift(F, 19)
            F = E
            E = P0(tt2)
        V ^= ((A << 224) + (B << 192) + (C << 160) + (D << 128) + (E << 96) + (F << 64) + (G << 32) + H)

    # 返回256比特结果（整数表示）
    return V

