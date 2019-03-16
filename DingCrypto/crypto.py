# -*- coding: utf-8 -*-

import base64
import hashlib
import struct
import string
import random
from Crypto import Random
from Crypto.Cipher import AES
from pkcs7 import PKCS7
import hmac


class DingTalkCrypto(object):
    def __init__(self, encode_aes_key, token, key):
        """
        钉钉加密、解密工具
        :param encode_aes_key: 数据加密密钥。用于回调数据的加密，长度固定为43个字符，从a-z, A-Z, 0-9共62个字符中选取
        :param token: 用于验证签名的 token
        :param key: key对于ISV开发来说，填写对应的suite_key，对于普通企业开发，填写企业的corp_id
        """
        self._encode_aes_key = encode_aes_key
        self._token = token
        self._key = key
        self._cipher = AES.new(self.aes_key, AES.MODE_CBC, self.iv_vector)
        self._pkcs7 = PKCS7(k=32)
        self._random = Random.new()

    def decrypt(self, encrypt_text):
        """
        解密钉钉加密数据
        :param encrypt_text: encoded text
        :return: rand_str, length, msg, corp_id
        """
        aes_msg = base64.decodestring(encrypt_text.encode('utf8'))
        pkcs7_text = self._cipher.decrypt(aes_msg)
        text = self._pkcs7.decode(pkcs7_text)
        rand_str = text[:16]  # 16字节随机字符串
        length, = struct.unpack('!i', text[16:20])  # 4字节数据长度
        msg_end_pos = 20 + length
        msg = text[20:msg_end_pos]
        key = text[msg_end_pos:]
        return rand_str, length, msg, key

    def encrypt(self, text):
        """
        将给定的本文采用钉钉的加密方式加密
        :param text: text
        :return: encrypt text
        """
        #modified on 2019.3.15
        rand_str = self.get_random_str()
        #rand_str = self._random.read(16) 
        length = self._length(text)
        full_text = rand_str.encode() + length + (text + self._key).encode()
        
        pkcs7_text = self._pkcs7.encode(full_text)
        aes_text = self._cipher.encrypt(pkcs7_text)
        #b = base64.encodestring(aes_text)
        b = base64.b64encode(aes_text)
        return b.decode('utf8')

    @staticmethod
    def _length(text):
        """
        获取4字节的消息长度
        :param text: text
        :return: four bytes binary ascii length of text
        """
        l = len(text)
        return struct.pack('!i', l)

    def check_signature(self, encrypt_text, timestamp, nonce, signature):
        """
        验证传输的信息的签名是否正确
        :param encrypt_text: str
        :param timestamp: str
        :param nonce: str
        :param signature: 签名
        :return: boolean
        """
        new_signature = self._make_signature(encrypt_text, timestamp, nonce, self._token)
        return new_signature == signature

    def get_random_str(self):
        """ 随机生成16位字符串
        @return: 16位字符串
        """
        #rule = string.letters + string.digits
        rule = string.ascii_letters + string.digits
        
        str = random.sample(rule, 16)
        return "".join(str)

    def sign(self, encrypt_text, timestamp, nonce):
        """
        给加密的信息生成签名
        :param encrypt_text: str
        :return: signature, timestamp, nonce
        """
        token = self._token
        signature = self._make_signature(encrypt_text, timestamp, nonce, token)
        return signature, timestamp, nonce

    def _make_signature(self, encrypt_text, timestamp, nonce, token):
        """
        生成签名
        :param encrypt_text: str
        :param timestamp: str
        :param nonce: str
        :param token: str
        :return: str
        """
        hash_str = ''.join(sorted([token, timestamp, nonce, encrypt_text]))
        obj = hashlib.sha1(hash_str.encode())
        return obj.hexdigest()

    @property
    def aes_key(self):
        src = self._encode_aes_key + '='
        return base64.decodestring(src.encode())#modified on 2019.3.15

    @property
    def iv_vector(self):
        return self.aes_key[:16]
