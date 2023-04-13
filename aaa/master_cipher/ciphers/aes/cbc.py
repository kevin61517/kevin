from .aes import _AES, AES, attrs, AESMessage, pad, unpad, typed, Valid
from types import FunctionType, MethodType

_MODE = AES.MODE_CBC


@attrs
class _CBC(_AES, mode=_MODE):

    iv = typed(str, default='', validator=Valid.pass_if_type(bytes, str))

    def _init_args(self):
        if not self.iv:
            raise ValueError('Missing init arguments iv.')
        key = self.key if isinstance(self.key, bytes) else self.key.encode()
        iv = self.iv if isinstance(self.iv, bytes) else self.iv.encode()
        return key, iv

    def _pre_encrypt(self, message: AESMessage):
        message.data = pad(
            message.data if isinstance(message.data, bytes) else message.data.encode('utf-8'),
            self.block_size,
            style=self.padding
        )

    def _encrypt(self, message: AESMessage):
        key, iv = self._init_args()
        message.result = AES.new(key, _MODE, iv).encrypt(message.data)

    def _decrypt(self, message: AESMessage):
        key, iv = self._init_args()
        message.result = AES.new(key, _MODE, iv).decrypt(message.data)

    def _post_decrypt(self, message: AESMessage):
        # 移除空格
        message.result = unpad(message.result, self.block_size, style=self.padding)
        # 還原
        message.result = str(message.result, encoding='utf-8').rstrip(b'\x00'.decode())

