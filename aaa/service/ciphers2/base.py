import json
from abc import ABC
from decimal import Decimal
from datetime import datetime
from attr import attrs, attrib

import base64
from .tools import Valid

ALGORITHMS: dict = {}  # 註冊的演算法


@attrs(slots=True, kw_only=True)
class BaseMessage:
    # 原始資料 Ex: 預加密、解密的訊息、預簽名資源
    data = attrib(default=b'', validator=Valid.pass_if(bytes, str))
    # 處理完成的資料 Ex: 已加密、解密的訊息、簽完名的結果
    result = attrib(default=None)
    # 進行驗證的簽名 Ex: 我們生成的簽名
    our_sign = attrib(default=None)
    # 被驗證的簽名 Ex: 三方的簽名
    target_sign = attrib(default=None)


class BaseCipher:
    """密碼基類"""

    init_message = BaseMessage

    @classmethod
    def __init_subclass__(cls, algo_name='', **kws):
        if not algo_name:
            raise ValueError('Missing argument algo_name')
        super().__init_subclass__(**kws)
        ALGORITHMS[algo_name.lower()] = cls

    def _pre_encrypt(self, message: BaseMessage): raise NotImplementedError
    def _encrypt(self, message: BaseMessage): raise NotImplementedError
    def _post_encrypt(self, message: BaseMessage): raise NotImplementedError
    def _pre_decrypt(self, message: BaseMessage): raise NotImplementedError
    def _decrypt(self, message: BaseMessage): raise NotImplementedError
    def _post_decrypt(self, message: BaseMessage): raise NotImplementedError
    def _pre_sign(self, message: BaseMessage): raise NotImplementedError
    def _sign(self, message: BaseMessage): raise NotImplementedError
    def _post_sign(self, message: BaseMessage): raise NotImplementedError
    def _pre_verify(self, message: BaseMessage): raise NotImplementedError
    def _verify(self, message: BaseMessage): raise NotImplementedError
    def _post_verify(self, message: BaseMessage): pass

    @classmethod
    def init(cls, *args, **kws):
        """回傳實例"""
        return cls(*args, **kws)

    def encrypt(self, message: BaseMessage) -> BaseMessage:
        """
        加密實作
        self._pre_encrypt() 加密前期處理
        self._encrypt() 加密
        self._post_encrypt() 加密後期處理
        :param message:
        :return:
        """
        print('message===>', message)
        if not isinstance(message, BaseMessage):
            message = self.init_message(data=message)
        self._pre_encrypt(message)
        self._encrypt(message)
        self._post_encrypt(message)
        return message

    def decrypt(self, message: BaseMessage) -> BaseMessage:
        """
        解密實作
        self._pre_decrypt() 解密前期處理
        self._decrypt() 解密
        self._post_decrypt() 解密後期處理
        :param message:
        :return:
        """
        if not isinstance(message, BaseMessage):
            message = self.init_message(data=message)
        self._pre_decrypt(message)
        self._decrypt(message)
        self._post_decrypt(message)
        return message

    def sign(self, message: BaseMessage) -> BaseMessage:
        if not isinstance(message, BaseMessage):
            message = self.init_message(data=message)
        self._post_sign(message)
        self._sign(message)
        self._post_sign(message)
        return message

    def verify_sign(self, message: BaseMessage) -> bool:
        if not isinstance(message, BaseMessage):
            raise TypeError('Message object must be type BaseMessage.')
        if not message.our_sign:
            raise ValueError('Missing arguments our_sign.')
        if not message.target_sign:
            raise ValueError('Missing arguments target_sign.')
        self._pre_verify(message)
        self._verify(message)
        self._post_verify(message)
        return bool()


