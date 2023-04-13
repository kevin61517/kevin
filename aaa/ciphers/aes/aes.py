import base64
from ..base import BaseCipher, Message, Valid, ABC, typed, attrs
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

_ALGO = 'AES'
_MODES: dict = {}


@attrs(slots=True, kw_only=True)
class AESMessage(Message):
    # 計數器(GCM模式)
    mac = typed(bytes, default=b'', validator=Valid.pass_if_type(bytes))
    hdr = typed(bytes, default=b'', validator=Valid.pass_if_type(bytes))


@attrs
class _AES(BaseCipher, ABC, algo_name=_ALGO):
    """AES算法"""

    init_message = typed(AESMessage, default=AESMessage)
    key = typed(bytes, default=b'', validator=Valid.pass_if_type(bytes, str))
    padding = typed(str, default='pkcs7')
    block_size = typed(int, default=AES.block_size, validator=Valid.pass_if_type(int))

    @classmethod
    def __init_subclass__(cls, mode=None, **kws):
        if mode is None:
            raise ValueError('Missing arguments mode.')
        if _MODES.get(mode):
            raise ValueError('This mode instance already exist.')
        _MODES[mode] = cls

    @classmethod
    def init(cls, mode, *args, **kws):
        """回傳實作"""
        try:
            return _MODES[mode](*args, **kws)
        except KeyError:
            raise NotImplementedError('This mode not implemented.')

    def _post_encrypt(self, message: AESMessage):
        """加密後期(可依不同需求實作)"""
        message.result = base64.b64encode(message.result).decode()

    def _pre_decrypt(self, message: AESMessage):
        """解密前期(可依不同需求實作)"""
        message.data = base64.b64decode(message.data.replace(r'\n', '\n').replace(' ', '+'))

