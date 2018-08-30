import urllib.request
import json


class BDIPSearch:
    def __init__(self,ipData):
        self.ipData = str(ipData)

    def getIP(self):
        url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?query=" + self.ipData + "&co=&resource_id=6006&t=1529809984888&ie=utf8&oe=gbk&format=json&tn=baidu"
        ipData = urllib.request.urlopen(url).read().decode("gbk")
        return json.loads(ipData)["data"]