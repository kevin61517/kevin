from ..base import *
from Cryptodome.Cipher import AES as AES_
from Cryptodome.Util.Padding import pad, unpad

__MODES__: dict = {}
__ALGO__ = 'AES'


@attrs(slots=True, kw_only=True)
class AESMessage(BaseMessage):
    # 計數器(GCM模式)
    mac = attrib(default=b'', validator=Valid.pass_if(bytes))
    hrd = attrib(default=b'', validator=Valid.pass_if(bytes))


@attrs
class AESBase(BaseCipher, ABC, algo_name='AES'):
    """AES基類、管理類"""

    init_message = AESMessage

    @classmethod
    def __init_subclass__(cls, mode=None, **kws):
        if mode is None:
            raise ValueError('Missing arguments mode.')
        if __MODES__.get(mode):
            raise ValueError('This mode already implemented.')
        __MODES__[mode] = cls

    @classmethod
    def init(cls, mode, *args, **kws):
        """回傳子類實作"""
        try:
            return __MODES__[mode](*args, **kws)
        except KeyError:
            raise NotImplementedError('This mode not implemented.')

    def _post_encrypt(self, message: BaseMessage):
        message.result = base64.b64encode(message.result).decode()

