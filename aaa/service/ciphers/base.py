"""
加密算法完成實例：
class Algorithm:
    encrypt = Encrypt()
    decrypt = Decrypt()
    signer = Signer()
    verifier = Verifier()
"""
import json
from abc import ABC
from decimal import Decimal
from datetime import datetime
from attr import attrs, attrib

__ENCRYPTS__: dict = {}  # 加密器實作
__DECRYPTS__: dict = {}  # 解密器實作
__SIGNERS__: dict = {}  # 簽名實作
__VERIFIERS__: dict = {}  # 驗簽實作
ALGORITHMS: dict = {}  # 已註冊的演算法


class _JSONEncoder(json.JSONEncoder):
    """
    json序列化器
    :class:`JSONEncoder` which respects objects that include the
    :class:`JsonSerializer` mixin.
    """
    def default(self, obj):
        types_ = {
            set: lambda e: list(e),
            Decimal: lambda e: str(e),
            datetime: lambda e: str(e),
            'd': super().default,
        }
        return types_.get(type(obj), 'd')(obj)


@attrs
class _CipherBase:
    """密碼器基類"""

    __json_encoder__ = _JSONEncoder

    def __call__(self, *args, **kws):
        raise NotImplementedError

    def _json_dumps(self, source):
        """序列化"""
        return json.dumps(source, cls=self.__json_encoder__)

    @staticmethod
    def _json_loads(source):
        """反序列化"""
        return json.loads(source)

    @staticmethod
    def pre_source(source):
        """初始化前處理"""
        return source

    @staticmethod
    def post_source(source):
        """初始化後處理"""
        return source

    def init_key(self):
        """初始化密鑰"""
        raise NotImplementedError

    def init_cipher(self):
        """初始化加解密器"""
        raise NotImplementedError

    @staticmethod
    def encode(source):
        """編碼Ex: b46, utf8"""
        return source

    @staticmethod
    def decode(source):
        """反編碼Ex: 反b64, utf8"""
        return source


@attrs
class EncryptBase(_CipherBase, ABC):
    """加密基類"""

    @classmethod
    def __init_subclass__(cls, algo_name='', **kws):
        if not algo_name:
            raise ValueError('Missing argument algo_name')
        super().__init_subclass__(**kws)
        __ENCRYPTS__[algo_name.lower()] = cls

    def __call__(self, source):
        """調用口
        1.初始化被加密物件
        2.初始化密鑰
        3.初始化加密器
        4.加密訊息
        5.回傳
        :param source:
        :return:
        """
        s = self._init_source(source)
        self.init_key()
        encrypt = self.init_cipher()
        cipher_text = encrypt(s)
        return self._final_process(cipher_text)

    def _init_source(self, source):
        """
        初始化被加密的物件
        1.初始化前處理
        2.序列化
        3.序列化後處理
        """
        s = self.pre_source(source)
        _s = self._json_dumps(s)
        return self.post_source(_s)

    def _final_process(self, cipher_text):
        """密文最後處理
        Ex: b64, utf8編碼
        """
        return self.encode(cipher_text)


@attrs
class DecryptBase(_CipherBase, ABC):
    """解密基類"""

    @classmethod
    def __init_subclass__(cls,  algo_name='', **kws):
        if not algo_name:
            raise ValueError('Missing argument algo_name')
        super().__init_subclass__(**kws)
        __DECRYPTS__[algo_name.lower()] = cls

    def __call__(self, source):
        """調用口
        1.預處理被解密物件
        2.初始化密鑰
        3.初始化解密器
        4.解密訊息
        5.解密後處理
        6.回傳
        :param source:
        :return:
        """
        s = self._init_source(source)
        self.init_key()
        decrypt = self.init_cipher()
        plain_text = decrypt(s)
        return self._final_process(plain_text)

    def _init_source(self, source):
        """初始化
        1.密文前期處理 Ex: 移除空格、+、=等等等等
        2.密文反編碼 Ex: 反b64, utf8...
        :param source:
        :return:
        """
        s = self.pre_source(source)
        return self.decode(s)

    def _final_process(self, plain_text):
        """明文最後處理
        1.未知問題處理 Ex: \x00(不可視空格)
        2.反序列化
        :param plain_text: 明文
        """
        _plain_text = self.post_source(plain_text)
        return self._json_loads(_plain_text)


@attrs
class SignBase(_CipherBase, ABC):
    """簽名基類"""
    @classmethod
    def __init_subclass__(cls,  algo_name='', **kws):
        if not algo_name:
            raise ValueError('Missing argument algo_name')
        super().__init_subclass__(**kws)
        __SIGNERS__[algo_name.lower()] = cls

    def exec(self): ...


@attrs
class VerifyBase(_CipherBase, ABC):
    """驗簽基類"""
    @classmethod
    def __init_subclass__(cls,  algo_name='', **kws):
        if not algo_name:
            raise ValueError('Missing argument algo_name')
        super().__init_subclass__(**kws)
        __VERIFIERS__[algo_name.lower()] = cls

    def exec(self): ...


class AlgorithmBase:
    """
    演算法基類
    1.註冊
    2.實作掛載
    """

    @classmethod
    def __init_subclass__(cls, algo_name='', **kws):
        if not algo_name:
            raise ValueError('Missing must argument algo_name.')
        super().__init_subclass__(**kws)
        _n = algo_name.lower()
        cls.__e = __ENCRYPTS__.get(_n, lambda *a, **b: NotImplemented)
        cls.__d = __DECRYPTS__.get(_n, lambda *a, **b: NotImplemented)
        cls.__s = __SIGNERS__.get(_n, lambda *a, **b: NotImplemented)
        cls.__v = __VERIFIERS__.get(_n, lambda *a, **b: NotImplemented)
        ALGORITHMS[_n] = cls

    def __init__(self, *args, **kws):
        self.encrypt = self.__e(*args, **kws)
        self.decrypt = self.__d(*args, **kws)
        self.sign = self.__s(*args, **kws)
        self.verify_sign = self.__v(*args, **kws)
