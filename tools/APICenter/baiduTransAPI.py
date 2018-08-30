import urllib.request
import urllib.parse
import json
import execjs

class BDTranslate:
    def __init__(self,content):
        self.content = content

    def getResult(self,typeNum=1):
        url = "http://fanyi.baidu.com/v2transapi"

        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BIDUPSID=4BC34E02F9E37FE9050EB4F9440189D3; PSTM=1500044981; BAIDUID=4A8AF2A1A420E9FC66FB6A0AC8FF950A:FG=1; __cfduid=dd5798a7820fc114394e3ff5f4eacac811521372255; MCITY=-%3A; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1528549342; BDSFRCVID=zK8sJeC62iEXkT372gOg-OqiaedALbvTH6aoRIXylk3cdE9m4Zq6EG0PDx8g0Kub1acuogKKKgOTHI6P; H_BDCLCKID_SF=tR4eVC-htCD3fP36q4vEh4P8bMrXetJyaR32abvbWJ5TMC_wh5Q5Kl3WX-jeaUuJtR630bn55hbxShPC-x78LtvWhJJb3jOIQCQlh4053l02Vhbae-t2ynQDQGQwB-RMW20e0h7mWIb_VKF4DT0hj53bjaRf-b-XMInKBRRVHJO_bncKMnbkbfJBDxr7Lb3lJRv8-xJTBC-aJCD45UrRbjK7yajK2bOiymv0VCJLLn658U5pKTQpQT8rKtFOK5OibCrrLM5uab3vOIOTXpO1j-CreGtjqT0tfnPsL-35HJREDRvNb-r_q4tehH483jOeWDTm5-nTtKI-jPL6WbOShptpXpjrbJOKMTrz3K3utK05OCFle5tMj6oyDGRf-b-XJR4j0TrE5CkaOlORy4oTj6D1-tjg5jtfW2cUhtouJl5AsRbPjP5c3MvB-fnAb53L2CJJVU7TLMKaExnXQft20M0AeMtjBbQaX2oWhJ7jWhk5ep72y5O_05TXja-Dq6LHtR303JjObPK_Hn7zen5zebtpbt-qJJjZBTnu2K3c3f32qxFGQq6JyP_P04nnBT5Ka56zbljnJjC2hJOT-tQqWxLkQN3TbRkO5bRiLRoSalR6Dn3oyTbJXp0njMTTqjDetRPtVCP-f-3bfTrn-J3H-4tBqxby26nKygJeaJ5nJDoCDIj4bPKbyUKVyq5ztxQz520tahu5QpP-HJ7s3CcVLpIgjfbrb-6xan7uKl0MLPjYbb0xynoD-jL1jfnMBMPe52OnaIb8LIFKMD-wj6LMjTPjheTqaRjaa5-X3b7Ef-cvb-O_bf--D4FkWMRnJ5-H52OMsl7h2Rjqehjs-Rjxy5K_hn5AXncQ2b720pKXaCbAqDQHQT3mQbvbbN3i-4DDKC7tWb3cWhvJ8UbSyjjme4tX-NFqJT8OJfK; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1529849076; to_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; PSINO=7; locale=zh; H_PS_PSSID=1434_21116_20929; from_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22it%22%2C%22text%22%3A%22%u610F%u5927%u5229%u8BED%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D",
            "Host": "fanyi.baidu.com",
            "Origin": "http://fanyi.baidu.com",
            "Pragma": "no-cache",
            "Referer": "http://fanyi.baidu.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        inputData = self.content

        with open("tools/APICenter/baidujs.js") as f:
            jsData = f.read()

        p = execjs.compile(jsData).call("e",inputData)

        if typeNum == 1:
            fromData = "en"
            toData = "zh"
        else:
            fromData = "zh"
            toData = "en"

        formData = {
            "from": fromData,
            "to": toData,
            "query": inputData,
            "transtype": "realtime",
            "simple_means_flag": "3",
            "sign": p,
            "token": "bc93f1684f9206bbed79a96652f50c20",
        }


        return json.loads(urllib.request.urlopen(
            urllib.request.Request(
                url=url,
                data=urllib.parse.urlencode(formData).encode("utf-8"),
                headers = headers,
            )
        ).read().decode("utf-8"))