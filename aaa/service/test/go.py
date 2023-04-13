from service.ciphers import ciphers


def test():
    rsa = ciphers.rsa(key='jojo')
    aes = ciphers.aes(key='abcd1234', iv='testiv')
    print(ciphers.algorithms())
    print(rsa.encrypt('kevin'))
    print(aes.encrypt('Lulu'))
