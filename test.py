# -*- coding: utf-8 -*-
# __author__ = 'seaside6'

import requests
import json
from crypto import DingTalkCrypto


random_token = '01234565789'
aes_key = '21cq6q1gsl59sh5oyjxauygcitsboxxccc02xr2zgpb'
corpid = 'ding90c5413cc3718b5e35c2f4657eb6xxxxx'
access_token = 'xxxx'
call_back_tags = ['user_add_org', 'user_modify_org', 'user_leave_org']
url = 'http://xxx.vaiwan.com/dingding/call_back_url'


def register_call_back_interface(random_token, aes_key, url, call_back_tags):
    """
    注册回调接口
    :param random_token: 在钉钉模型上的 token 随机填写
    :param aes_key:  在钉钉模型上的 aes_key 随机生成的 43位 aes_key
    :param url:  ‘填写要回调的URL地址’
    :param call_back_tags: ‘填写要回调的事件’
    :return:
    """
    data = {
        "call_back_tag": call_back_tags,
        "token": random_token,
        "aes_key": aes_key,
        "url": url
    }
    header = {'Content-Type': 'application/json'}
    token_dict = {'access_token': access_token}
    res = requests.post("https://oapi.dingtalk.com/call_back/register_call_back",
                        headers=header,
                        params=token_dict,
                        data=json.dumps(data))
    print(res.json())
    try:
        return res.json()['errcode']
    except:
        self.__raise_error(res)


#@app.route('/dingtalk/call_back_url',methods=['POST'])#类似Flask等框架下使用
def dingding_call_back(request_json, request_args):#测试时可模拟钉钉的请求参数
    dingcrypto = DingTalkCrypto(aes_key, random_token, corpid)
    rand_str, length, msg, key = dingcrypto.decrypt(request_json.get('encrypt').encode('utf8'))

    safe_msg = eval(msg)#safe_eval
    event_type = safe_msg.get('EventType') 
    if event_type != 'check_url' and event_type != 'debug_callback':
        print('Event type error!')

    signature_get, timestamp_get, nonce_get = request_args.get('signature'),\
        request_args.get('timestamp'), request_args.get('nonce')
    dingcrypto = DingTalkCrypto(aes_key, random_token, corpid)
    encrypt = dingcrypto.encrypt("success").decode('utf8')
    signature, timestamp, nonce = dingcrypto.sign(encrypt, timestamp_get, nonce_get)
    script_response = {
        'msg_signature': signature,
        'timeStamp': timestamp_get,
        'nonce': nonce_get,
        'encrypt': encrypt
        }
    return script_response


if __name__ == "__main__":
    return_val = register_call_back_interface(random_token, aes_key, url, call_back_tags)
    if return_val != 0:
        print('Register call back error!')

    request_args = {'signature':'xxxx', 'timestamp':'1552640489665', 'nonce':'ORQWdfs6'}
    request_json = {'encrypt' :'xxxx'}
    response = dingding_call_back(request_json, request_args)
    print(response) 