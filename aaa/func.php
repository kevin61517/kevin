<?php
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
