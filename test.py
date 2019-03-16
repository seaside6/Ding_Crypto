# -*- coding: utf-8 -*-
# __author__ = 'seaside6'

import requests
import json
from DingCrypto.crypto import DingTalkCrypto

# 钉钉官方给的测试数据
# https://open-doc.dingtalk.com/microapp/faquestions/ltr370
encrypt_text = "1a3NBxmCFwkCJvfoQ7WhJHB+iX3qHPsc9JbaDznE1i03peOk1LaOQoRz3+nlyGNhwmwJ3vDMG+OzrHMeiZI7gTRWVdUBmfxjZ8Ej23JVYa9VrYeJ5as7XM/ZpulX8NEQis44w53h1qAgnC3PRzM7Zc/D6Ibr0rgUathB6zRHP8PYrfgnNOS9PhSBdHlegK+AGGanfwjXuQ9+0pZcy0w9lQ=="

aes_key = '4g5j64qlyl3zvetqxz5jiocdr586fn2zvjpa8zls3ij'
token = '123456'
corpid = 'suite4xxxxxxxxxxxxxxx'

signature = '5a65ceeef9aab2d149439f82dc191dd6c5cbe2c0'
timestamp = '1445827045067'
nonce = 'nEXhMP4r'


crypto = DingTalkCrypto(aes_key, token, corpid)

class TestCrypto:
    def test_encrypt(self):
        content = 'success'
        encrypt_msg = crypto.encrypt(content)
        randstr, length, msg, suite_key = crypto.decrypt(encrypt_msg)
        assert msg.decode() == content

    def test_decrypt(self):
        randstr, length, msg, suite_key = crypto.decrypt(encrypt_text)
        msg = json.loads(msg)

        assert msg['EventType'] == 'check_create_suite_url'
        assert msg['Random'] == 'LPIdSnlF'
        assert suite_key.decode() == 'suite4xxxxxxxxxxxxxxx'

    def test_check_signature(self):
        assert crypto.check_signature(encrypt_text, timestamp, nonce, signature)

    def test_sign(self):
        actual_sig, actual_time, actual_nonce = crypto.sign(encrypt_text, timestamp, nonce)
        assert signature == actual_sig


if __name__ == "__main__":
	test = TestCrypto()
	test.test_encrypt()
	test.test_decrypt()
	test.test_sign()
	test.test_check_signature()