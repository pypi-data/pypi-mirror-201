"""
#=============================================================================
#
#     Filename: easy_aes.py
#      Summary: pip install pycrypto
#               使用 CBC 模式
#               测试: https://tools.lami.la/jiami/aes
#
#       Author: dantezhu
#        Email: dantezhu@qq.com
#     Homepage: http://www.vimer.cn
#
#      Created: 2019-01-08 21:29:21
#      Version: 0.0.1
#      History:
#               0.0.1 | dantezhu | 2019-01-08 21:29:21 | init
#
#=============================================================================
"""

from Crypto.Cipher import AES


class EasyAES:
    """封装AES，使用cbc模式"""

    _key = None
    _iv = None
    _mode = None

    def __init__(self, key, iv):
        """
        key 必须是bytes，长度必须为 128/192/256位，即16/24/32字节
        iv 必须是bytes，长度必须位 128位，即16字节
        """
        self._key = key
        self._iv = iv

    def encrypt(self, src):
        """
        src必须是bytes
        """
        # 填充字符
        padding = AES.block_size - len(src) % AES.block_size
        # 每段明文在加密前都会添加一个 1-16 字节的 pad，使总长度膜 16 余 0。
        # pad 的长度由 pad 的最后一个字节描述
        src = src + padding * bytes(chr(padding), encoding='utf8')

        aes = AES.new(self._key, AES.MODE_CBC, self._iv)
        return aes.encrypt(src)

    def decrypt(self, src):
        """
        src必须是bytes
        """
        aes = AES.new(self._key, AES.MODE_CBC, self._iv)
        dst = aes.decrypt(src)
        if not dst:
            return None

        return dst[0:-dst[-1]]
