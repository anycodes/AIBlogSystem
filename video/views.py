from django.shortcuts import render,redirect
import album.models
import video.models
from BlogSystem.information import Information
from currency.views import webLogger, ipCounter, errorLogger, isLoginTrue, filterTags
# Create your views here.

def videoContent(request):

    try:
        # 获取信息，记录log
        information = Information()
        pageInformation = information.getAll()
        webLogger(request.META)
        try:
            userIP = request.META["HTTP_X_FORWARDED_FOR"]
        except:
            userIP = request.META["REMOTE_ADDR"]
        if ipCounter(userIP, information.getValue("maxCounter")):
            category = video.models.VideoModel.objects.all().order_by("-vid")
            tempList = []
            try:
                for eveTemp in category:
                    videoDataTitle = eveTemp.titleList
                    videoDataUrl = eveTemp.urlList
                    if "&title&" in videoDataTitle:
                        videoDataTitle = videoDataTitle.split("&title&")
                    else:
                        videoDataTitle = [videoDataTitle]

                    if "&url&" in videoDataUrl:
                        videoDataUrl = videoDataUrl.split("&url&")
                    else:
                        videoDataUrl = [videoDataUrl]

                    returnData = []
                    for i in range(0, len(videoDataTitle)):
                        returnData.append((videoDataTitle[i], videoDataUrl[i]))
                    tempList.append((eveTemp.name,returnData,eveTemp.vid))
                category = tempList
            except:
                pass
            return render(request, "video/%s/%s" % (information.getValue("templatesVideoName"), "index.html"), locals())
        else:
            return redirect("/sorry")
    except Exception as e:
        errorLogger(e)
        request.session["errorNumber"] = "100004"
        return redirect("/wrong")