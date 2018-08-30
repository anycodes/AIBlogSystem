from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from currency.views import webLogger, ipCounter, errorLogger, isLoginTrue, filterTags
import usercenter.models
from artificialIntelligence.Article import ArticleHandle
import json
import hashlib
import urllib.request
import urllib.parse
import time
import base64
import os
import ssl
import tools.APICenter.baiduIPSearch
import tools.APICenter.baiduTransAPI
# Create your views here.


# hash
def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


@csrf_exempt
def apiAuth(request):
    ssl._create_default_https_context = ssl._create_unverified_context
    # # 119服务器
    # webLogger(request.META)
    # if request.method == "POST":
    #
    #     secretId = request.POST.get("secretid")
    #     secretKey = request.POST.get("secretKey")
    #
    #     tempData = {
    #         "secretid": secretId,
    #         "secretKey": secretKey,
    #         "action": request.POST.get("action"),
    #         "body": request.POST.get("body")
    #     }
    #
    #     # API的地址
    #     url = "http://139.199.16.182:8001/api"
    #
    #     # 对数据进行处理
    #     reqData = urllib.parse.urlencode(tempData).encode("utf-8")
    #
    #     # 构建request对象
    #     req = urllib.request.Request(url=url, data=reqData)
    #
    #     # 发起请求，获得response
    #     res = urllib.request.urlopen(req).read().decode("utf-8")
    #
    #     return HttpResponse(res)

    # 139服务器
    try:
        webLogger(request.META)
    except Exception as e:
        print(e)
    if request.method == "POST":

        secretId = request.POST.get("secretid")
        secretKey = request.POST.get("secretKey")

        userList = usercenter.models.UserModel.objects.filter(username=secretId)
        for eveUserData in userList:
            if md5((str(md5(str(eveUserData.password).encode("utf-8"))) + "=!liuyublog-liuyublog!=" + str(md5(str(eveUserData.username).encode("utf-8")))).encode("utf-8")) != secretKey:
                return JsonResponse({
                    "code":-1,
                    "status":"auth error",
                })

        # 鉴权完成

        action = request.POST.get("action")
        if not action:
            return JsonResponse({
                "code": -3,
                "status": "no action error",
            })

        body = request.POST.get("body")
        if not body:
            return JsonResponse({
                "code": -3,
                "status": "no body error",
            })


        # 文本摘要
        if action == "ArticleAbstract":
            try:
                articleData = json.loads(body)["article"]
                numData = json.loads(body)["count"]
                try:
                    numData = json.loads(body)["count"]
                    if not numData:
                        numData = 5
                except Exception as e:
                    errorLogger(e)
                    numData = 5
                tempArticle = ArticleHandle(articleData)
                return JsonResponse({
                    "code":0,
                    "status":"success",
                    "response":{
                        "result":tempArticle.getAbstract(numData)
                    }
                })

            except Exception as e:
                print(e)
                errorLogger(e)
                return JsonResponse({
                    "code": -10001,
                    "status": "body error",
                })


        # 关键词提取
        if action == "ArticleKeyword":
            try:
                articleData = json.loads(body)["article"]
                try:
                    numData = json.loads(body)["count"]
                    if not numData:
                        numData = 5
                except Exception as e:
                    errorLogger(e)
                    numData = 5
                tempArticle = ArticleHandle(articleData)
                return JsonResponse({
                    "code": 0,
                    "status": "success",
                    "response": {
                        "result": tempArticle.getKeywords(numData)
                    }
                })

            except Exception as e:
                errorLogger(e)
                return JsonResponse({
                    "code": -10001,
                    "status": "body error",
                })


        # 图像识别
        if action == "ImagePrediction":
            try:
                imageBase = json.loads(body)
                imageData = imageBase["image"]
                tempData = str(md5((str(time.time()) + imageData).encode("utf-8")))
                pathInputData = "tools/imageAI/cache/" + tempData + ".jpg"

                print(pathInputData)

                with open(pathInputData, "wb") as f:
                    f.write(base64.b64decode(imageData))

                pfile = os.popen("python3 tools/imageAI/imageAIHandle.py %s 2"%(os.path.join(os.getcwd(),pathInputData)))
                return JsonResponse({
                    "code": 0,
                    "status": "success",
                    "response": {
                        "result":pfile.read().replace("\n","")
                    }
                })

            except Exception as e:
                print(e)
                return JsonResponse({
                    "code": -10001,
                    "status": "body error",
                })

        # 图像标注
        if action == "ObjectDetection":
            try:
                imageBase = json.loads(body)
                imageData = imageBase["image"]
                tempData = str(md5((str(time.time()) + imageData).encode("utf-8")))
                pathInputData = "tools/imageAI/cache/" + tempData + ".jpg"

                print(pathInputData)

                with open(pathInputData, "wb") as f:
                    f.write(base64.b64decode(imageData))

                pfile = os.popen("python3 tools/imageAI/imageAIHandle.py %s 1"%(os.path.join(os.getcwd(),pathInputData)))
                jsonData = json.loads(pfile.read().replace("\n",""))
                return JsonResponse({
                    "code": 0,
                    "status": "success",
                    "response": {
                        "result":{
                            "image":jsonData["baseData"],
                            "content":jsonData["result"]
                        }
                    }
                })

            except Exception as e:
                print(e)
                return JsonResponse({
                    "code": -10001,
                    "status": "body error",
                })


        # ip查询
        if action == "IPSearch":
            try:
                ipData = json.loads(body)["ip"]
                returnData = tools.APICenter.baiduIPSearch.BDIPSearch(ipData).getIP()
                if returnData:
                    return JsonResponse({
                        "code": 0,
                        "status": "success",
                        "response": {
                            "result": returnData[0]
                        }
                    })
                else:
                    return JsonResponse({
                        "code": -20001,
                        "status": "ip error",
                    })

            except Exception as e:
                print(e)
                errorLogger(e)
                return JsonResponse({
                    "code": -10001,
                    "status": "body error",
                })


        # 百度翻译
        if action == "Translate":
            try:
                content = json.loads(body)["content"]
                try:
                    typenumber = int(json.loads(body)["type"])
                except:
                    typenumber = 1

                returnData = tools.APICenter.baiduTransAPI.BDTranslate(content).getResult(typenumber)

                if returnData:
                    return JsonResponse({
                        "code": 0,
                        "status": "success",
                        "response": {
                            "result": returnData
                        }
                    })
                else:
                    return JsonResponse({
                        "code": -20001,
                        "status": "centent error",
                    })

            except Exception as e:
                print(e)
                errorLogger(e)
                return JsonResponse({
                    "code": -10001,
                    "status": "body error",
                })


    else:
        return JsonResponse({
            "code": -2,
            "status": "method error",
        })

