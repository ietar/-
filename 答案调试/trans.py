import urllib.request
import urllib.parse
import json
import zlib

import time
import random
import hashlib


class YouDaoFanYi:

    def __init__(self):
        self.url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36",
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"_ntes_nnid=c686062b6d8c9e3f11e2a8413b5bb9a8,1517022642199; OUTFOX_SEARCH_USER_ID_NCOO=1367486017.479911; OUTFOX_SEARCH_USER_ID=722357816@10.168.11.24; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; JSESSIONID=abcCzqE6R9jTv5rTtoWgw; fanyi-ad-id=40789; fanyi-ad-closed=1; ___rl__test__cookies=1519344925194",
            "Referer":"http//fanyi.youdao.com/",
            "X-Requested-With": "XMLHttpRequest"
        }

        self.data = {
            "from":"AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTIME",
            "typoResult": "false"
        }

        self.client = 'fanyideskweb'
        self.secretKey = 'ebSeFb%=XZ%T[KZ)c(sy!'

    @staticmethod
    def readData(resp):
        info = resp.info()
        encoding = info.get('Content-Encoding')
        transferEncoding = info.get('Transfer-Encoding:')
        if transferEncoding != 'chunked' and encoding != 'gzip':
            return resp.read()
        str1 = ""
        while True:
            chunk = resp.read(4096)
            if not chunk: break
            decomp = zlib.decompressobj(16 + zlib.MAX_WBITS)
            data = decomp.decompress(chunk)
            str1 = str1 + data.decode("utf-8")
        return str1

    def translate(self, content):
        data = dict(self.data)
        salt = str(int(time.time() * 1000) + random.randint(1, 10))
        sign = hashlib.md5((self.client + content + salt + self.secretKey).encode('utf-8')).hexdigest()

        data["client"] = self.client
        data["salt"] = salt
        data["sign"] = sign
        data["i"]=content

        data = urllib.parse.urlencode(data).encode('utf-8')
        request = urllib.request.Request(url=self.url, data=data, headers=self.headers, method='POST')
        response = urllib.request.urlopen(request)
        #result=response.read()
        #print(result)
        result = YouDaoFanYi.readData(response)
        response.close()
        dictResult = json.loads(result)

        paragraphs=[]
        for paragraph in dictResult["translateResult"]:
            line=""
            for a in paragraph:
                line = line + a["tgt"]

            if(len(line) != 0):
                paragraphs.append(line)

        return paragraphs


#有道翻译中，是支持翻译多段落文章的，所以调用translate之后，会返回一个数组，数组里的元素就是翻译过后的段落。输入几个段落，输出就有几个段落。

content = input('请输入需要翻译的单词：').replace("\\n", "\n")

print(YouDaoFanYi().translate(content))
