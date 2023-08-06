import base64
import random

from .easy_aes import EasyAES
from ...share.log import logger


class TokenHelper:

    secret = None

    block_size = 16

    def __init__(self, secret):
        """
        secret: AES key,  must be either 16, 24, or 32 bytes long
        """
        self.secret = self._convert_str_to_bytes(secret)

    def encode(self, src: bytes):
        """
        1. 使用aes_cbc方法将源串src加密成串dst
        2. 之后将iv与dst拼成token。
            token的格式为 前16位 固定为iv，剩下的部分为token。

        3. 之后将token进行base64加密方便http传输

        :param src:
        :return: 加密后base64字符串。为方便传输，类型为str。
        """
        iv = self._convert_str_to_bytes(self._gen_rand_str(self.block_size))

        aes = EasyAES(
            self.secret,
            iv
        )

        encrypt_bytes = aes.encrypt(src)

        packed_bytes = iv + encrypt_bytes

        base64_result = base64.b64encode(packed_bytes)

        return base64_result.decode('utf8')

    def decode(self, token: bytes):
        """
        解析token
        :param token:
        :return: 被加密的bytes。
        """

        packed_bytes = base64.b64decode(token)

        iv = packed_bytes[:self.block_size]
        encrypt_bytes = packed_bytes[self.block_size:]

        aes = EasyAES(
            self.secret,
            iv
        )

        decrypt_bytes = aes.decrypt(encrypt_bytes)

        if not decrypt_bytes:
            logger.info('decrypt fail. token: %s', token)
            return None

        return decrypt_bytes

    def _gen_rand_str(self, length):
        """
        generate secret key，参考django
        不区分大小写，因为mysql的unique不区分大小写
        """
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        return ''.join([random.choice(chars) for i in range(length)])

    def _convert_str_to_bytes(self, src):
        """
        转换str为bytes
        bytes => bytes
        str => bytes
        else => str => bytes
        """

        return src if isinstance(src, bytes) else bytes(src, 'utf8')
