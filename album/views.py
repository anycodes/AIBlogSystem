from django.shortcuts import render,redirect
import album.models
import currency.models
import random
from BlogSystem.information import Information
from currency.views import webLogger, ipCounter, errorLogger, isLoginTrue, filterTags
# Create your views here.

def albumContent(request):

    try:
        # 获取信息，记录log
        information = Information()
        pageInformation = information.getAll()
        webLogger(request.META)
        try:
            userIP = request.META["HTTP_X_FORWARDED_FOR"]
        except:
            userIP = request.META["REMOTE_ADDR"]


        loginId = isLoginTrue(request)
        try:
            isloginData = True
            userId = loginId[2]

        except Exception as e:
            errorLogger(e)
            isloginData = False


        if ipCounter(userIP, information.getValue("maxCounter")):
            category = currency.models.CategoryModel.objects.filter(type="3")

            aid = request.GET.get("aid")
            if aid:
                categoryData = category.get(cid=aid)
                pictureData = album.models.ImagesModel.objects.filter(album=categoryData,is_recommend=True).order_by("-iid")
            else:
                pictureData = list(album.models.ImagesModel.objects.filter(is_recommend=True).order_by("-iid"))
                random.shuffle(pictureData)
                pictureData = pictureData[0:20]
            return render(request, "album/%s/%s" % (information.getValue("templatesAlbumName"), "index.html"), locals())
        else:
            return redirect("/sorry")
    except Exception as e:
        errorLogger(e)
        request.session["errorNumber"] = "100004"
        return redirect("/wrong")