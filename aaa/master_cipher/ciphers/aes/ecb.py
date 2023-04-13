from .aes import _AES, AES, attrs, AESMessage, pad, unpad

_MODE = AES.MODE_ECB


@attrs
class _ECB(_AES, mode=_MODE):

    def _pre_encrypt(self, message: AESMessage):
        message.data = pad(
            message.data if isinstance(message.data, bytes) else message.data.encode('utf-8'),
            self.block_size,
            style=self.padding
        )

    def _encrypt(self, message: AESMessage):
        key = self.key if isinstance(self.key, bytes) else self.key.encode()
        message.result = AES.new(key, _MODE).encrypt(message.data)

    def _decrypt(self, message: AESMessage):
        key = self.key if isinstance(self.key, bytes) else self.key.encode()
        message.result = AES.new(key, _MODE).decrypt(message.data)

    def _post_decrypt(self, message: AESMessage):
        # 移除空格
        message.result = unpad(message.result, self.block_size, style=self.padding)
        # 還原
        message.result = str(message.result, encoding='utf-8').rstrip(b'\x00'.decode())
