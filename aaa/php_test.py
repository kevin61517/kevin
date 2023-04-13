import signal
import os
from subprocess import PIPE, STDOUT, Popen
import json


class Php:
    """PHP"""

    @staticmethod
    def _exec(php_code: str):
        """執行器"""
        process = Popen(['php'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, close_fds=True)
        output = process.communicate(php_code.encode())[0]
        try:
            os.kill(process.pid, signal.SIGTERM)
        except:
            pass
        return json.loads(output)

    @staticmethod
    def test():
        process = ...

    def rsa_decrypt(self, cipher_text, key, key_type) -> str:
        """RSA公鑰解密"""
        code = """<?php
function formatPublicKey($publicKey) {
    return "-----BEGIN PUBLIC KEY-----\n" . wordwrap($publicKey , 64, "\n", true) . "\n-----END PUBLIC KEY-----";
}

function formatPrivateKey($privateKey) {
    return "-----BEGIN RSA PRIVATE KEY-----\n" . wordwrap($privateKey , 64, "\n", true) . "\n-----END RSA PRIVATE KEY-----";
}

function rsaDecrypt($source, $type, $key) {
    $maxlength = 128;
    $output = '';
    while ($source) {
        $input = substr($source, 0, $maxlength);
        $source = substr($source, $maxlength);
        if ($type == 'private') {
            $ok = openssl_private_decrypt($input, $out, $key);
        } else {
            $ok = openssl_public_decrypt($input, $out, $key);
        }
        $output .= $out;
    }
    return $output;
}
$key = '%s';
$cipher_text = '%s';
$key_type = '%s';

if ($key_type == 'private') {
    $key = formatPrivateKey($key);
    $type = 'private';
} else {
    $key = formatPublicKey($key);
    $type = 'public';
}

$result = rsaDecrypt(base64_decode($cipher_text), $type, $key);
echo $result;
""" % (key, cipher_text, key_type)
        return self._exec(php_code=code)


php = Php()
