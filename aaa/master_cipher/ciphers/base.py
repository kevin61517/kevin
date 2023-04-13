from abc import ABC
from types import MethodType
from attr import attrs
from payment.typed import typed
from .tools import Valid

ALGORITHMS: dict = {}  # 註冊的演算法


@attrs(slots=True, kw_only=True)
class Message:
    """訊息(可依照不同算法實作變異)"""
    # 原始資料 Ex: 預加密、解密的訊息、預簽名資源
    data = typed(str, default=b'', validator=Valid.pass_if_type(bytes, str))
    # 處理完成的資料 Ex: 已加密、解密的訊息、簽完名的結果
    result = typed(str, default=None)
    # 進行驗證的資料 Ex: 我們生成的簽名
    verify_source = typed(str, default=None)
    # 被驗證的簽名 Ex: 三方的簽名
    target_sign = typed(str, default=None)


@attrs
class BaseCipher:
    """密碼基類"""

    init_message = typed(Message, default=Message)

    @classmethod
    def __init_subclass__(cls, algo_name='', **kws):
        if not algo_name:
            raise ValueError('Missing argument algo_name')
        super().__init_subclass__(**kws)
        ALGORITHMS[algo_name.lower()] = cls

    @classmethod
    def init(cls, *args, **kws):
        """回傳實例"""
        return cls(*args, **kws)

    def encrypt(self, message: Message) -> Message:
        """加密"""
        if not isinstance(message, Message):
            message = self.init_message(data=message)
        self._pre_encrypt(message)
        self._encrypt(message)
        self._post_encrypt(message)
        return message

    def decrypt(self, message: Message) -> Message:
        """解密"""
        if not isinstance(message, Message):
            message = self.init_message(data=message)
        self._pre_decrypt(message)
        self._decrypt(message)
        self._post_decrypt(message)
        return message

    def sign(self, message: Message) -> Message:
        """簽名"""
        if not isinstance(message, Message):
            message = self.init_message(data=message)
        self._pre_sign(message)
        self._sign(message)
        self._post_sign(message)
        return message

    def verify_sign(self, source, sign) -> Message:
        """驗簽"""
        types_ = str, bytes
        if not isinstance(source, types_):
            raise TypeError(f'Local arguments source must be type str or bytes, not {source.__class__}.')
        if not isinstance(sign, types_):
            raise TypeError(f'Local arguments sign must be type str or bytes, not {sign.__class__}.')
        message = self.init_message(verify_source=source, target_sign=sign)
        self._pre_verify(message)
        self._verify(message)
        self._post_verify(message)
        return message

    def _pre_encrypt(self, message: Message):
        """加密前期處理"""
        raise NotImplementedError

    def _encrypt(self, message: Message):
        """加密"""
        raise NotImplementedError

    def _post_encrypt(self, message: Message):
        """加密後期處理"""
        raise NotImplementedError

    def _pre_decrypt(self, message: Message):
        """解密前期處理"""
        raise NotImplementedError

    def _decrypt(self, message: Message):
        """解密"""
        raise NotImplementedError

    def _post_decrypt(self, message: Message):
        """解密後期處理"""
        raise NotImplementedError

    def _pre_sign(self, message: Message):
        """簽名前期處理"""
        raise NotImplementedError

    def _sign(self, message: Message):
        """簽名"""
        raise NotImplementedError

    def _post_sign(self, message: Message):
        """簽名後期處理"""
        raise NotImplementedError

    def _pre_verify(self, message: Message):
        """驗簽前期處理"""
        raise NotImplementedError

    def _verify(self, message: Message):
        """驗簽"""
        raise NotImplementedError

    def _post_verify(self, message: Message):
        """驗簽後期處理"""
        pass


