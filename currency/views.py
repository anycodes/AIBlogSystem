from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from BlogSystem.information import Information
from tools.everydaySentence.Sentence import Sentence
import datetime
import os.path
import usercenter.models
import re
import random
import hashlib

# Create your views here.

def wrongNumber(number):
    wrongDict = {
        "100001": "页面错误",
        "100002": "权限错误",
        "100003": "数据请求错误",
        "100004": "内部错误",
        "100009": "文章不对外开放，您的访问超出权限",
    }
    return wrongDict[number]

def getFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    with open(filename,'rb') as f:
        while True:
            b = f.read()
            if not b :
                break
            myhash.update(b)
    return myhash.hexdigest()

# hash
def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def newTime():
    timeData = datetime.datetime.now()
    return (timeData.year, timeData.month, timeData.day, timeData.hour, timeData.minute, timeData.second)

def webLogger(requestMeta):
    timeData = newTime()
    logPath = 'logger/access/%s/%s' % (timeData[0], timeData[1])
    try:
        try:
            userIP = requestMeta["HTTP_X_FORWARDED_FOR"]
        except:
            userIP = requestMeta["REMOTE_ADDR"]
    except:
        userIP = None
    try:
        userAgent = requestMeta["HTTP_USER_AGENT"]
    except:
        userAgent = None
    try:
        pathInfor = requestMeta["PATH_INFO"]
    except:
        pathInfor = None
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    with open('%s/%s.log' % (logPath, timeData[2]), 'a') as f:
        f.write("%s:%s:%s\t%s\t%s\t%s\n" % (timeData[3], timeData[4], timeData[5], userIP, userAgent, pathInfor))

def errorLogger(exception):
    timeData = newTime()
    logPath = 'logger/error/%s/%s' % (timeData[0], timeData[1])
    exception = ",".join(str(exception).split("\n"))
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    with open('%s/%s.log' % (logPath, timeData[2]), 'a') as f:
        f.write("%s:%s:%s\t%s\n" % (timeData[3], timeData[4], timeData[5], exception))

def ipCounter(ipData, maxCounter):
    timeData = newTime()
    logPath = 'logger/access/%s/%s/%s.log' % (timeData[0], timeData[1], timeData[2])
    counter = 0
    if os.path.exists(logPath):
        with open(logPath) as f:
            loggerData = f.readlines()
        for eveLoggerData in loggerData:
            if eveLoggerData:
                eveIPData = eveLoggerData.strip().split('\t')[1]
                if eveIPData == ipData:
                    counter = counter + 1
        if counter > int(maxCounter):
            return False
    return True

def sendEmail(username, email, content):
    import smtplib
    information = Information()
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.header import Header
    try:
        title = content[0]
        text = content[1]
        sender = email
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = Header("Liu Yu", 'utf-8')
        msgRoot['To'] = Header(username, 'utf-8')
        subject = title
        msgRoot['Subject'] = Header(subject, 'utf-8')
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        mail_msg = text
        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
        try:
            server_con = smtplib.SMTP_SSL(information.getValue("emailSMTP"), information.getValue("emailPort"))
            server_con.login(information.getValue("emailUser"), information.getValue("emailPassword"))  # 登录服务器
            server_con.sendmail(information.getValue("emailUser"), sender, msgRoot.as_string())
            server_con.close()
            return True
        except Exception as e:
            errorLogger(e)
    except Exception as e:
        errorLogger(e)
    return False

# 过滤HTML中的标签
# 将HTML中标签等信息去掉
# @param htmlstr HTML字符串.
def filterTags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s

# 替换常用HTML字符实体.
# 使用正常的字符替换HTML中特殊的字符实体.
# 你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
# @param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr

def isUserTrue(username,password,email):
    try:
        userData = usercenter.models.UserModel.objects.get(username=username,password=password,email=email)
        if userData.type == "1":
            return (1, userData.uid)
        else:
            return (2, userData.uid)
    except Exception as e:
        return 0

def isLoginTrue(request):
    try:
        requestSession = request.session["login"]
        userType,userInfor = requestSession.split("-",1)
        userUid,UserInfor = userInfor.split("-",1)
        userData = usercenter.models.UserModel.objects.get(uid=userUid)
        if "%s-%s-%s" % (userData.username, userData.password, userData.email) == UserInfor:
            return (1,userType,userUid)
        else:
            del request.session["login"]
            return 0
    except Exception as e:
        return -1

@csrf_exempt
def maxCounterIndex(request):
    information = Information()
    webtitle = information.getValue("webName")
    keywords = information.getValue("webKeyword")
    description = information.getValue("webDescription")

    isFirstTime = True
    title = "抱歉"
    if request.method == "POST":
        email = request.POST.get("email")

        sendEmail("管理员","service@52exe.cn",("来自用户的请求","收到了反爬虫解除请求，用户的邮箱是%s"%(email)))
        sendEmail("用户", email, ("来自刘宇的博客", "已经收到了您申请解除反爬虫限制的请求，请确保您的邮箱：%s是正确的。" % (email)))

        title = "感谢支持"
        isFirstTime = False

    return render(request, "currency/maxCounter/index.html", locals())

@csrf_exempt
def wrongPageIndex(request):

    try:
        information = Information()
        webtitle = information.getValue("webName")
        keywords = information.getValue("webKeyword")
        description = information.getValue("webDescription")

        isFirstTime = True
        errorNumber = request.session["errorNumber"]
        del request.session["errorNumber"]
        errorDescription = wrongNumber(errorNumber)

        return render(request, "currency/wrongPage/index.html", locals())
    except:
        request.session["errorNumber"] = "100004"
        return redirect("/wrong")

@csrf_exempt
def loginPage(request):
    information = Information()
    webtitle = information.getValue("webName")
    keywords = information.getValue("webKeyword")
    description = information.getValue("webDescription")

    try:
        isLogin = isLoginTrue(request)
        if isLogin[0] == 1:
            if isLogin[1] == "1":
                return redirect("/admin/index")
            if isLogin[1] == "2":
                return redirect("/usercenter/index")
    except Exception as e:
        errorLogger(e)

    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        loginData = isUserTrue(username, password, email)

        if  loginData == 0:
            wrongMessage = "登陆失败！请检查信息是否正确！"
        elif loginData[0] == 1:
            request.session["login"] = "%d-%d-%s-%s-%s" % (loginData[0],loginData[1], username, password, email)
            redirectTitle = "管理员登陆成功"
            redirectUrl = "/admin/index"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            request.session["login"] = "%d-%d-%s-%s-%s" % (loginData[0],loginData[1], username, password, email)
            redirectTitle = "用户登陆成功"
            redirectUrl = "/index"
            return render(request, "currency/loginAndRegister/handle.html", locals())

    return render(request, "currency/loginAndRegister/login.html", locals())

def logoutPage(request):
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            return redirect("/login")
        else:
            del request.session["login"]
            redirectTitle = "注销成功"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        return redirect("/login")

@csrf_exempt
def registerPage(request):
    information = Information()
    webtitle = information.getValue("webName")
    keywords = information.getValue("webKeyword")
    description = information.getValue("webDescription")

    try:
        isLogin = isLoginTrue(request)
        if isLogin[0] == 1:
            if isLogin[1] == "1":
                redirectTitle = "您已经登陆，无需重复登录"
                redirectUrl = "/admin/index"
                return render(request, "currency/loginAndRegister/handle.html", locals())
            if isLogin[1] == "2":
                redirectTitle = "您已经登陆，无需重复登录"
                redirectUrl = "/usercenter/index"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        errorLogger(e)

    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")
        email = request.POST.get("email")
        qq = request.POST.get("qq")
        phone = request.POST.get("phone")

        photoFile = random.choice([i for i in range(41)])

        try:
            if usercenter.models.UserModel.objects.all().count() == 0:
                type = "1"
            else:
                type = "2"
            usercenter.models.UserModel.objects.create(
                username = username,
                password = password,
                sex = "3",
                email = email,
                qq = qq,
                phone = phone,
                type = type,
                state = "1",
                photo = "/files/userFace/%d.jpg" % (photoFile)
            )
            redirectTitle = "注册成功"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        except Exception as e:
            wrongMessage = "注册失败！用户名等信息已被占用！"
            errorLogger(e)
    return render(request, "currency/loginAndRegister/register.html", locals())


def webIndex(request):
    try:

        if "android" in str(request.META["HTTP_USER_AGENT"]).lower():
            phoneData = "true"
        if "iphone" in str(request.META["HTTP_USER_AGENT"]).lower():
            phoneData = "true"

        # 获取信息，记录log
        information = Information()
        pageInformation = information.getAll()
        webLogger(request.META)

        # 每日一句
        sentenceData = Sentence()
        (sentence, author) = sentenceData.getOneSentence()
        sentence = sentence[0:-1]

        numData = [x for x in range(1, 192)]
        picNum = random.choice(numData)

        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            webIndexData = 0 # 未登陆
        else:
            webIndexData = 1 # 已登陆
        try:
            userIP = request.META["HTTP_X_FORWARDED_FOR"]
        except:
            userIP = request.META["REMOTE_ADDR"]
        if ipCounter(userIP, information.getValue("maxCounter")):
            return render(request,"currency/indexPage/index.html",locals())
        else:
            return redirect("/sorry")
    except Exception as e:
        print(e)
        errorLogger(e)
        request.session["errorNumber"] = "100004"
        return redirect("/wrong")
