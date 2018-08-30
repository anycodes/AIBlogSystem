from django.shortcuts import render
from BlogSystem.information import Information
from currency.views import webLogger, ipCounter, errorLogger, isLoginTrue, filterTags

from django.views.decorators.csrf import csrf_exempt
from tools.everydaySentence.Sentence import Sentence
import currency.models
from apicenter.views import md5
# Create your views here.

def userIndex(request):
    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "请登录之后再进行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
        # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 获取信息，记录log
    information = Information()
    pageInformation = information.getAll()
    webLogger(request.META)
    nav = 'index'
    pagetitle = "仪表盘"
    userData = currency.models.UserModel.objects.get(uid=isLogin[2])
    articleData = currency.models.ArticleModel.objects.all().order_by("-aid")
    comments = currency.models.CommentsModel.objects.all()
    tempComments = []
    for eve in comments.filter(username=userData.username, usertype=1):
        tempComments.append((eve,comments.filter(pid=eve.cid)))
    if comments.filter(username=userData.username, usertype=1).count() > 6:
        articleData = articleData[0:comments.filter(username=userData.username, usertype=1).count()]
    else:
        articleData = articleData[0:6]

    return render(request, "usercenter/%s/%s" % (information.getValue("templatesUserCenterName"), "index.html"), locals())

def userAPI(request):
    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "请登录之后再进行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
        # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 获取信息，记录log
    information = Information()
    pageInformation = information.getAll()
    webLogger(request.META)
    nav = 'api'
    pagetitle = "API中心"
    userData = currency.models.UserModel.objects.get(uid=isLogin[2])
    secretid = userData.username
    secretkey = md5((str(md5(str(userData.password).encode("utf-8"))) + "=!liuyublog-liuyublog!=" + str(md5(str(userData.username).encode("utf-8")))).encode("utf-8"))
    return render(request, "usercenter/%s/%s" % (information.getValue("templatesUserCenterName"), "api.html"),locals())

@csrf_exempt
def userInfor(request):

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "请登录之后再进行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
        # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。


    if request.method == "POST":
        '''
        email	service@52exe.cn
        password	liuyuliuyu
        phone	13500993691
        photo	/files/userFace/39.jpg
        qq	
        sex	男
        username	liuyu
        wechat	None
        '''
        try:
            userData = currency.models.UserModel.objects.get(uid=isLogin[2])
            email = request.POST.get("email",userData.email)
            password = request.POST.get("password",userData.password)
            phone = request.POST.get("phone",userData.phone)
            photo = request.POST.get("photo",userData.photo)
            qq = request.POST.get("qq",userData.qq)
            sex = request.POST.get("sex",userData.sex)
            wechat = request.POST.get("wechat",userData.wechat)

            currency.models.UserModel.objects.filter(uid=isLogin[2]).update(
                photo = photo,
                phone = phone,
                qq = qq,
                sex = sex,
                wechat = wechat,
                email = email,
                password = password
            )
            status = "修改成功"
        except:
            status = "修改失败"

    userData = currency.models.UserModel.objects.get(uid=isLogin[2])

    # 获取信息，记录log
    information = Information()
    pageInformation = information.getAll()
    webLogger(request.META)
    nav = 'setting'

    pagetitle = "个人信息"

    photoFile = []
    for evePhoto in range(1, 41):
        photoFile.append((evePhoto, "/files/userFace/%d.jpg" % (evePhoto)))



    return render(request, "usercenter/%s/%s" % (information.getValue("templatesUserCenterName"), "infor.html"), locals())