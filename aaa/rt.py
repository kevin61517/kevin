from Crypto.PublicKey import RSA
# RSA = __import__('Crypto.PublicKey.RSA')#, fromlist=[''])
from Crypto.Cipher import PKCS1_v1_5
import base64


data = {'data': 'hvF0VPQSk3nJ4kyJxt9hcPYZsY8H9QR220Z6hsxVQiIZSpmwavG5DDUiKrTev4gFT0/K+L37A1qiNd4QWmPWW4oeSARfuG/+bFD9IZg4R+6yUCSfdXqBqTk+p27Yd5j7nK353X3TCCpP4S9P07Yvx+BYU80T1pD3zEejZXoIXgc=', 'merchNo': 'A11337'}
public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChsziQcHqOo0kqPsCP//QKdw2BnpEGuFCe/z25PP/yWfHILqx2S9VUxscwhEA0Xz4Vi1PhKReydpVA2tBYcglDsvtjQCAbRoOQtYDYl+PqKOgMJnlgHgpQ2siNL22H8079AenDz797OiLQBYUiAIMNZ4HA/RQD4xqBHQfVJySJjwIDAQAB'
rsa_key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'


def decrypt_with_public_key(ciphertext, pubkey):
    key = RSA.importKey(pubkey)
    cipher = PKCS1_v1_5.new(key)
    ciphertext = base64.b64decode(ciphertext)
    decrypted = cipher.decrypt(ciphertext, None)
    return decrypted.decode('utf-8')


if __name__ == '__main__':
    print(decrypt_with_public_key(data.get('data'), rsa_key))