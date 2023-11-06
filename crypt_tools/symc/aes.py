
from crypt_tools.symc.fund import *

class aes:
    k = None
    k_lst = None

    def __init__(self, length="L-128"):
        self.k = key_generate(length)
        self.k_lst = key_ext(self.k, BOX[0], length)

    def key_update(self, k, length="L-128"):
        self.k = k
        self.k_lst = key_ext(self.k, BOX[0], length)

    def encrypt(self, msg, mode=0, roud=1):
        msg = "0x"+msg.encode().hex()
        for _ in range(roud):
            msg = roud_fuc(self.k_lst, msg, mode)
        return msg

