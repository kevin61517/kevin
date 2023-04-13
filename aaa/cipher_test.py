from ciphers import cipher, AES

if __name__ == '__main__':
    print(cipher.rsa())
    print(cipher.aes(AES.MODE_ECB, padding='pkcs5'))
