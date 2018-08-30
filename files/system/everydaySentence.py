import urllib.request
import json

import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

def writeToFile(ename,term):
    with open("everydaySentence.data","a") as f:
        f.write("%s----%s\n"%(ename,term))

pageNum = 8

while True:
    urlData = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?from_mid=1&format=json&ie=utf-8&oe=utf-8&subtitle=%E6%A0%BC%E8%A8%80&query=%E6%A0%BC%E8%A8%80&rn=8&pn=" + str(pageNum) + "&resource_id=6844"
    jsonData = json.loads(urllib.request.urlopen(urlData).read().decode("utf-8"))
    thisPageCount = 0
    for eveData in jsonData["data"][0]['disp_data']:
        thisPageCount = thisPageCount + 1
        ename = eveData["ename"]
        term = eveData["term"]
        print("%s----%s"%(ename,term))
        writeToFile(ename, term)
    if thisPageCount < 8:
        break
    else:
        pageNum = pageNum + 8

print("完成名人名言采集！")