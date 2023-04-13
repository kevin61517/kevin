import rsa
import base64
from Crypto.PublicKey import RSA


def zfillStrToBin(s):
    b = bytes(s.encode())
    for i in range(117 - len(b)):
        b += b'\x00'
    print(len(b))
    return b


class RsaNopadding:

    def __init__(self, key):
        self.pubkey = RSA.importKey(base64.b64decode(key))

    def encrypt(self, message):
        kLen = rsa.common.byte_size(self.pubkey.n)
        msg = zfillStrToBin(message)
        _b = rsa.transform.bytes2int(msg)
        _i = rsa.core.encrypt_int(_b, self.pubkey.e, self.pubkey.n)
        result = rsa.transform.int2bytes(_i, kLen)
        return result.hex()






# message='{"code":"123451","clienttime":1564560057}'
# msg = RsaNopadding("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD2DT4odzkDd7hMlZ7djdZQH12j38nKxriINW1MGjMry3tXheya113xwmbBOwN0GA4zTwKFauFJRzcsD0nDFq1eaatcFKeDF25R4dnQRX+4BdTwFVS8lIb8nJMluSBwK+i4Z3VF+gfZ0AqQOXda6lJ4jPBt9Ep7VXEAHXUDn9JM8wIDAQAB")
# print(msg.encrypt(message))

# import rsa
# import base64
# from Crypto.PublicKey import RSA
#
#
# class Encrypt:
#     def encrypt(self, source, key):
#         # rsa_pubkey = rsa.PublicKey(mm, ee)
#         k = '-----BEGIN PRIVATE KEY-----\n' + key + '\n-----END PRIVATE KEY-----'
#         rsa_pubkey = RSA.importKey(k)
#         crypto = self._encrypt(source.encode(), rsa_pubkey)
#         return crypto.hex()
#
#     def _pad_for_encryption(self, message, target_length):
#         # message = message[::-1]
#         max_msglength = target_length - 11
#         msglength = len(message)
#         print("msglength==" + str(msglength))
#         padding = message
#         padding_length = target_length - msglength
#         for i in range(padding_length):
#             padding += b'\x00'
#         return b''.join([padding])
#
#     def _encrypt(self, message, pub_key):
#         keylength = rsa.common.byte_size(pub_key.n)
#         padded = self._pad_for_encryption(message, keylength)
#         payload = rsa.transform.bytes2int(padded)
#         encrypted = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
#         block = rsa.transform.int2bytes(encrypted, keylength)
#
#         return block
#
#     def str_to_hex(self, s):
#         return ' '.join([hex(ord(c)).replace('0x', '') for c in s])

# import rsa
# import base64
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# #rsa encryption, usually base64 encoding the encrypted result
#
#
# def handle_pub_key(key):
#     """
#     Handling the public key
#     Public key format pem, processed into a format beginning with -----BEGIN PUBLIC KEY----- and ending with -----END PUBLIC KEY-----
#     :param key: the public key in pem format, without-----BEGIN PUBLIC KEY-----beginning,-----END PUBLIC KEY-----end
#     :return:
#     """
#     start = '-----BEGIN PRIVATE KEY-----\n'
#     end = '-----END PRIVATE KEY-----'
#     result = ''
#     # Split the key, change a line every 64 bits
#     divide = int(len(key)/64)
#     divide = divide if (divide> 0) else divide + 1
#     line = divide if (len(key)% 64 == 0) else divide + 1
#     for i in range(line):
#         result += key[i * 64:(i + 1) * 64] +'\n'
#     result = start + result + end
#     return result
#
#
# def get_param(message, public_key):
#     """
#     Processing long messages without this processing report the following error
#     OverflowError: 458 bytes needed for message, but there is only space for 117
#     :param message
#     :param public_key public key
#     :return:
#     """
#     pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
#     crypto = b''
#     divide = int(len(message)/117)
#     divide = divide if (divide> 0) else divide + 1
#     line = divide if (len(message)% 117 == 0) else divide + 1
#     for i in range(line):
#         crypto += rsa.encrypt(message[i * 117:(i + 1) * 117].encode(), pubkey)
#
#     crypto1 = base64.b64encode(crypto)
#     return crypto1.decode()



# if __name__ =='__main__':
#     message = 'amount=20000&mno=A211214211648017&orderno=1234567894&pt_id=1&time=2021-12-15 16:14:26'
#     pri = 'MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAODFnnVetlPN4lFChd5Kz3lrdWzCXesFOaXugGtHpJSnWq7eX0wrBVHZ/S2qB/OS98RzJ/+5hmcXDOEZTvPvg1Z4K7En35HN/AuoaKm3gKaCdAqN5EQTMPf+A394dR7BR3AIvDSrRHYUc6gxBm9rjB8vC8cUth9FD2Ut8AGg59kLAgMBAAECgYEAoozn+pODIfobuI52R3ssre+TnRK3XvaJaUGhJ3RJRqP8xcfVfT0DfN075mE3nOPlQPHStHJUC4u06bkmyuykunHpLA//F8yZ7ekFhH0BY9k9mXbL7pR9RjlQFZv3R2x1R4Rpi5l5O1D6OgJJT4B31BNePyv/6enoZzW9OS3jhSECQQD0uvDb19klUVK89kFm5MvvnsjE7PF2gaj2CuJ1K6tIoBomQM+AIlR21EPs+ZdkX3cv7QyX2uBE8D8zDB1zGcHxAkEA6x9lLJqZALjh0Ge1vccFzvhO73GSJCXLsU3Fvp/vt05mvoIdTtfNuEaSJec1PGt3Yf29Ns94swfutOQUsDwOuwJAb9YiDYUFMX2JXtr2Jkw2OemI/Bz/d1VnXhC5TixHmOe5K3QAnyCREsCLzfZ9TZwmvlsInzihtj9H0k8eAiRqMQJBAIeHrFk+sC1jZP8tmOxQ2b9JEK8jJxthEf4dF3xfUt21+rGb7OryqGmtfDcPBHfUdpdsnPIIO8nvK6DnzCkeJVsCQG7hWXH0FdP4hxy5hYi+P0I3wnQAdBlv37Kq02XHWyMN0GprYYouS9jz5zqWl/XSLi/y29HijhGTSwRkI/bQW2A='
#     # public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQClsqQiK5KMBO88nf2CE6I5aGJQX9jTXorDveudfSKts2/5i/ipCLo68rl4gsPYwzjP5ef5IJTK0Xdzrrfkn5d2GCVA7n/jN3rlqjfSy1w2D4JqMUtqEhRQr7KfofZbZBnPOooiepRht + W0D9rIAceLLD5UPpstZ4lPCW2t/PG0hQIDAQAB"
#     public_key = handle_pub_key(pri)
#     param = get_param(message, public_key)
#     print(param)



pri = 'MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAODFnnVetlPN4lFChd5Kz3lrdWzCXesFOaXugGtHpJSnWq7eX0wrBVHZ/S2qB/OS98RzJ/+5hmcXDOEZTvPvg1Z4K7En35HN/AuoaKm3gKaCdAqN5EQTMPf+A394dR7BR3AIvDSrRHYUc6gxBm9rjB8vC8cUth9FD2Ut8AGg59kLAgMBAAECgYEAoozn+pODIfobuI52R3ssre+TnRK3XvaJaUGhJ3RJRqP8xcfVfT0DfN075mE3nOPlQPHStHJUC4u06bkmyuykunHpLA//F8yZ7ekFhH0BY9k9mXbL7pR9RjlQFZv3R2x1R4Rpi5l5O1D6OgJJT4B31BNePyv/6enoZzW9OS3jhSECQQD0uvDb19klUVK89kFm5MvvnsjE7PF2gaj2CuJ1K6tIoBomQM+AIlR21EPs+ZdkX3cv7QyX2uBE8D8zDB1zGcHxAkEA6x9lLJqZALjh0Ge1vccFzvhO73GSJCXLsU3Fvp/vt05mvoIdTtfNuEaSJec1PGt3Yf29Ns94swfutOQUsDwOuwJAb9YiDYUFMX2JXtr2Jkw2OemI/Bz/d1VnXhC5TixHmOe5K3QAnyCREsCLzfZ9TZwmvlsInzihtj9H0k8eAiRqMQJBAIeHrFk+sC1jZP8tmOxQ2b9JEK8jJxthEf4dF3xfUt21+rGb7OryqGmtfDcPBHfUdpdsnPIIO8nvK6DnzCkeJVsCQG7hWXH0FdP4hxy5hYi+P0I3wnQAdBlv37Kq02XHWyMN0GprYYouS9jz5zqWl/XSLi/y29HijhGTSwRkI/bQW2A='
pub = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDgxZ51XrZTzeJRQoXeSs95a3Vswl3rBTml7oBrR6SUp1qu3l9MKwVR2f0tqgfzkvfEcyf/uYZnFwzhGU7z74NWeCuxJ9+RzfwLqGipt4CmgnQKjeREEzD3/gN/eHUewUdwCLw0q0R2FHOoMQZva4wfLwvHFLYfRQ9lLfABoOfZCwIDAQAB'

message = 'amount=20000&mno=A211214211648017&orderno=1234567894&pt_id=1&time=2021-12-15 16:14:26'


msg = RsaNopadding(pri)
print(msg.encrypt(message))


# en = Encrypt()
# message = 'amount=20000&mno=A211214211648017&orderno=1234567894&pt_id=1&time=2021-12-15 16:14:26'
# print('密文：', en.encrypt(message, pri))
