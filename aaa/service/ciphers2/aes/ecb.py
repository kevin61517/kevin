from .base import *

__MODE__ = AES_.MODE_ECB


@attrs
class ECB(AESBase, mode=__MODE__):

    key = attrib()
    block_size = attrib(default=AES_.block_size)

    # def encrypt(self, message): print('== SUCCESS ==')

    @key.validator
    def _valid_key(self, _, value):
        if type(value) is not bytes:
            raise TypeError(f'Key must be type bytes, not {value.__class__.__name__}')

    def _pre_encrypt(self, message: BaseMessage):
        message.data = pad(
            message.data if type(message.data) is bytes else message.data.encode('utf-8'),
            self.block_size,
            style='pkcs7'
        )

    def _encrypt(self, message: BaseMessage):
        message.result = AES_.new(self.key, __MODE__).encrypt(message.data)

    # def _post_encrypt(self, message: BaseMessage):
    #     message.result = base64.b64encode(message.result).decode()

    def _pre_decrypt(self, message: BaseMessage):
        message.data = base64.b64decode(message.data.replace(r'\n', '\n').replace(' ', '+'))

    def _decrypt(self, message: BaseMessage):
        message.result = AES_.new(self.key, __MODE__).decrypt(message.data)

    def _post_decrypt(self, message: BaseMessage):
        # 移除空格
        message.result = unpad(message.result, self.block_size, style='pkcs7')
        # 還原
        message.result = str(message.result, encoding='utf-8').rstrip(b'\x00'.decode())