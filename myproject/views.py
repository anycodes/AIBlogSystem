from django.shortcuts import render,redirect
from BlogSystem.information import Information
from currency.views import webLogger, ipCounter, errorLogger, isLoginTrue, filterTags
# Create your views here.

def projectContent(request):

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
            return render(request, "project/%s/%s" % (information.getValue("templatesProjectName"), "index.html"), locals())
        else:
            return redirect("/sorry")
    except Exception as e:
        print(e)
        errorLogger(e)
        request.session["errorNumber"] = "100004"
        return redirect("/wrong")