"""
某招投标网站的AES、RSA加解密模拟
"""
import requests
import aes_rsa
import random
import json
import traceback
import pymongo

class ZhongSY:
    def __init__(self):
        self.url = 'https://www.cnpcbidding.com/cms/pmsbidInfo/listPageOut'
        self.headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Content-Type': 'application/json;charsetset=UTF-8',
            'Referer': 'https://www.cnpcbidding.com/html/1/index.html',
        }
        self.public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfXfMzgg4m5RRLg2vcrYBFN4sBhE1VtW1sBkXxC5wtCRaOZv0kudk9CIQfU6c+eEaaZKUnygxHWdSqdwURCE0IKgLcolXF+RHmu/rl977FfjRg9pAkBg5z05PfHDqWqkIsqX0iRaSP31BUZOgtwafbiBv2dBvRBMdq03ty4q8OQQIDAQAB"
        self.private_Key = "MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAITfvlC8+Nr+vz3DnhuCWW41ax8PG+rCiXt/f4XjRMlj9ZC2AuMMbtHLsTMLhCrhgHt1MxdcoYtqvQfxu4AVOh6pZrxMr2AiyNpw8SecmM3m0YWYNc7tnUB6/vlLyQduikD4qaxNiB5FcUiRpiRoLpz7rT6UV+/zDh+ibgvZRLDRAgMBAAECgYB7/mMV6tJ7YkBKPdK8Lw6PZq/5Att1XmZ3ZYo2Adg96tbMXN0izYZYprFMRhHnBhokm0C7K0jg1hFiaXUkWCqr83H+Y+DZ7js9NDhApPYAELQDIu288/nz34mjU/wnIGWP6WK5PCd1QjR8ltFay1TDLecdavHHjWGfHOMYnY5/dQJBAOZ4ICB+VrXMwR8KUR3r420YAHPwQDQKDetMHwgYHtFUH/k3CtKzPrltx103OhQcKyfrkoPj8SREZZISaBEQL6cCQQCTl+pjOSMud4hFTvfTnkGx9EZT3dBAv31ZfzHCu4g41FxRLyJLY6iKce069IhMjC2gfoLtwDLM/dKzRAuw9+rHAkAd9/zlfMg1t7xdFvBZXbUjGH3mlZUjrzMEJ8/ZM5m+SpwlwfyMTXaYkifcfTP2LXuHI2DX+an/t00l43LY1Sv9AkAEgQ5WGNhKArvV4aMOgjXfCGVdCdfhIfbhVFBgcPinQ1PN5nJVeqUaFH/43J2MOHrr+vBj8Qmb1+MmNV1l+SrhAkArJjCosjMI32RT3GmC6+gwxADR9Ib53yDHwRoMeO34dgK3hj3+e66Jhpcht3AjXBVs7bF9xzXcePpxxCka9cEv"

    def page_data(self,max_page):
        """ 页面申请原文生成器，生成请求信息的json字符串 """
        for i in range(1,max_page+1):
            page_information ={
                'categoryId': "199",
                'dataId': 'undefined',
                'pageNo': i,
                'pageSize': 15,
                'pid': "198",
                'projectType': "",
                'title': "",
                'url': "./list.html",
            }
            yield page_information

    def random_str(self,length):
        """ 生成指定长度的字符串 """
        base_str = 'abcdefghigklmnopqrstuvwxyz0123456789'
        random_list = [random.choice(base_str) for i in range(length)]
        random_str = ''.join(random_list)
        return random_str

    def encrypt_request_json(self, page_data, random_str):
        """ 模拟目标网站进行请求数据加密 """
        request_data = aes_rsa.aes_encrypt(page_data,random_str)
        encrypted = aes_rsa.rsa_encrypt(random_str,self.public_key)
        json_dict = {
            'requestData': request_data,
            'encrypted': encrypted,
        }
        return json_dict

    # 解密页面
    def decrypt_response_json(self,response):
        """ 先解密出key，再根据key解密出页面内容 """
        try:
            encrypted = response['encrypted']
            request_data = response['requestData']
        except Exception as e:
            traceback.print_exc()
            print('网页数据解析错误')
            return
        # 解密出AESkey
        aes_key= aes_rsa.rsa_decrypt(encrypted,self.private_Key)
        # 解密出页面内容
        response_data = aes_rsa.aes_decrypt(request_data,aes_key)
        return response_data

    def request_data(self,json):
        response = requests.post(self.url, headers=self.headers, json=json, verify=False)
        return response.json()

    def save_data(self,data):
        print(data)

    def run(self):
        page_data = self.page_data(3)
        for msg in page_data:
            msg_str = json.dumps(msg)
            random_str = self.random_str(16)
            # 加密请求信息
            request_json = self.encrypt_request_json(msg_str, random_str)
            print('开始请求网页。。。')
            response_json = self.request_data(request_json)
            result = self.decrypt_response_json(response_json)
            if not result:
                print('== get error page %s ==' % msg['pageNo'])
                continue
            print('成功解密数据')
            result_json = json.loads(result)
            information_list = result_json['list']
            self.save_data(information_list)

if __name__ == '__main__':
    spider = ZhongSY()
    spider.run()





