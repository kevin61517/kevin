from php import Php
from php_whisperer import read_raw, generate_php


config = Php.parse_ini_file("f.php")
t = Php.http_build_query({'name': 'kevin'})


if __name__ == '__main__':
    print('t===>', t)
    print(config, type(config))
    print(config["sectionName"]["keyName"])