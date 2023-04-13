import base64
import Cryptodome.Cipher.PKCS1_v1_5 as Cipher_pkcs1_v1_5
import Cryptodome.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from ..base import BaseCipher, attrs, Message, typed, Valid

_ALGO = 'RSA'


@attrs
class _RSA(BaseCipher, algo_name=_ALGO):
    """RSA算法"""
    # 公鑰
    public_key = typed(str, default='', validator=Valid.pass_if_type(str))
    # 私鑰
    private_key = typed(str, default='', validator=Valid.pass_if_type(str))
    # 長度
    length = typed(int, default=256, validator=Valid.pass_if_type(int))

    def _pre_encrypt(self, message: Message):
        """加密後期處理"""
        message.data = message.data.encode('utf-8') if type(message.data) is str else message.data

    def _encrypt(self, message: Message):
        """加密"""
        if not self.public_key:
            raise ValueError('Missing init arguments public_key.')
        length = message.data.__len__()
        default_length = 100
        key = RSA.importKey('-----BEGIN PUBLIC KEY-----\n' + self.public_key + '\n-----END PUBLIC KEY-----')
        _cipher = Cipher_pkcs1_v1_5.new(key)
        msg = message.data
        if length < default_length:
            """長度符合規範直接加密"""
            message.result = _cipher.encrypt(msg)
        else:
            """長度不符合規範，分開加密"""
            offset = 0
            result = []
            while length - offset > 0:
                if length - offset > default_length:
                    result.append(_cipher.encrypt(msg[offset:offset + default_length]))
                else:
                    result.append(_cipher.encrypt(msg[offset:]))
                offset += default_length
            message.result = b''.join(result)

    def _post_encrypt(self, message: Message):
        """加密後期處理"""
        message.result = base64.b64encode(message.result).decode('utf-8')

    def _pre_decrypt(self, message: Message):
        """解密前期處理"""
        message.data = base64.b64decode(message.data)

    def _decrypt(self, message: Message):
        """解密"""
        if not self.private_key:
            raise ValueError('Missing init arguments private_key.')
        length = message.data.__len__()
        default_length = self.length
        key = RSA.importKey('-----BEGIN RSA PRIVATE KEY-----\n' + self.private_key + '\n-----END RSA PRIVATE KEY-----')
        _cipher = Cipher_pkcs1_v1_5.new(key)
        msg = message.data
        sentinel = b'xyz'
        if length < default_length:
            """長度符合規範直接解密"""
            message.result = _cipher.decrypt(msg, sentinel)
        else:
            """長度不符合規範，分開解密"""
            offset = 0
            result = []
            while length - offset > 0:
                if length - offset > default_length:
                    result.append(_cipher.decrypt(msg[offset:offset + default_length], sentinel))
                else:
                    result.append(_cipher.decrypt(msg[offset:], sentinel))
                offset += default_length
            message.result = b''.join(result)

    def _post_decrypt(self, message: Message):
        """解密後期處理"""
        message.result = message.result.decode()

    def _pre_sign(self, message: Message):
        """簽名前期處理"""
        message.data = message.data.encode('utf-8') if isinstance(message.data, str) else message.data

    def _sign(self, message: Message):
        """簽名"""
        key = '-----BEGIN RSA PRIVATE KEY-----\n' + self.private_key + '\n-----END RSA PRIVATE KEY-----'
        cipher = sign_PKCS1_v1_5.new(RSA.importKey(key))
        msg_hash = SHA256.new(message.data)
        message.result = cipher.sign(msg_hash=msg_hash)

    def _post_sign(self, message: Message):
        """簽名後期處理"""
        message.result = base64.b64encode(message.result).decode()

    def _pre_verify(self, message: Message):
        """驗簽前期處理"""
        if isinstance(message.verify_source, str):
            message.verify_source = message.verify_source.encode('utf8')
        if isinstance(message.target_sign, str):
            message.target_sign = base64.b64decode(message.target_sign)

    def _verify(self, message: Message):
        """驗簽"""
        key = '-----BEGIN PUBLIC KEY-----\n' + self.public_key + '\n-----END PUBLIC KEY-----'
        cipher = sign_PKCS1_v1_5.new(RSA.importKey(key))
        msg_hash = SHA256.new(message.verify_source)
        message.result = cipher.verify(msg_hash, message.target_sign)
