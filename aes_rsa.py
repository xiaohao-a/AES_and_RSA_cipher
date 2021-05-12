"""
AES RSA 加密 解密
"""

from Cryptodome.Cipher import AES,PKCS1_v1_5
from Cryptodome.Util import Padding
from Cryptodome.PublicKey import RSA
import base64
import json

# rsa公钥加密
def rsa_encrypt(text,public_key):
    """
    通常js文件的rsa还原：js代码var key = CryptoJS.enc.Utf8.parse(keyStr)...
    :param text:字符串类型的待加密字符
    :param public_key:字符串类型的公钥去掉首尾标识字符部分
    :return:加密后的base64编码，通常网络通信的编码方案
    """
    public_key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
    rsakey = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsakey)
    cipher_text = cipher.encrypt(text.encode())
    cipher_text = base64.b64encode(cipher_text).decode()
    return cipher_text
# rsa私钥解密
def rsa_decrypt(text,privatekey):
    """
    rsa解密还原
    :param text: 字符串类型的待解密数据
    :param privatekey: 字符串类型的解密私钥，没有首尾标识字串
    :return: 解密后的字符串
    """
    privatekey = '-----BEGIN RSA PRIVATE KEY-----\n' + privatekey + '\n-----END RSA PRIVATE KEY-----'
    rsakey = RSA.importKey(privatekey)
    plain = PKCS1_v1_5.new(rsakey)
    text = base64.b64decode(text.encode())
    plain_text = plain.decrypt(text,b'0').decode()
    return plain_text

# aes加密ECB
def aes_encrypt(text,key):
    """
    还原了简单的aes加密，ECB模式，
    :param text: str待加密的字符串
    :param key: str加密key
    :return: str密文结果
    """
    aes = AES.new(key.encode(),AES.MODE_ECB)
    text_b = text.encode()
    pad_text = Padding.pad(text_b,AES.block_size,style='pkcs7')
    encrypt_text = aes.encrypt(pad_text)
    encrypt_text = base64.b64encode(encrypt_text).decode()
    return encrypt_text
# aes解密ECB
def aes_decrypt(text,key):
    """
    aes解密还原，ECB模式
    :param text:  str待解密的字符串密文
    :param key:  str秘钥
    :return:  解密后的字符串
    """
    aes = AES.new(key.encode(),AES.MODE_ECB)
    text = base64.b64decode(text.encode())
    plain_text = aes.decrypt(text)
    # pad后的数据可能在末尾加了字符，避免影响json识别，需进行unpad。
    plain_text = Padding.unpad(plain_text, AES.block_size, style='pkcs7').decode()
    return plain_text


if __name__ == '__main__':
    plain_key = "hys4cwwni105mjr5"
    result_01 = aes_encrypt('aes加密',plain_key)
    result_02 = aes_decrypt(result_01,plain_key)
    print('加密结果：',result_01)
    print('解密结果：',result_02)
