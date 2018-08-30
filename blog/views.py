from django.shortcuts import render
from django.shortcuts import redirect,reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import *
from BlogSystem.information import Information
from currency.views import webLogger,ipCounter
from tools.everydaySentence.Sentence import Sentence
from currency.views import webLogger, ipCounter, errorLogger, isLoginTrue, filterTags
from artificialIntelligence.Recommended import RecommendedHandle
from artificialIntelligence.Spam import SpamHandle
from django.db.models.aggregates import Count
from artificialIntelligence.SearchArticle import SearchArticleHandle
import re
import os
import random
import currency.models
import usercenter.models

# Create your views here.

def getDeafulatPic(content):
    pic_data = re.findall("<img(.*?)>", content)
    if pic_data:
        picUrl = re.findall('src="(.*?)"', pic_data[0])[0]
    else:
        picName = os.walk('files/upload/defaultBlogPic')
        nameList = []
        for eveName in picName:
            for eveFileName in eveName[2]:
                nameList.append(eveFileName)
        picData = random.choice(nameList)
        picUrl = "/files/defaultBlogPic/" + picData
    return picUrl

@cache_page(60 * 15, key_prefix="blogIndex")
def blogIndex(request):
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

            # 头部名人名言
            sentenceData = Sentence()
            (sentence, author) = sentenceData.getOneSentence()
            sentence = sentence[0:-1]


            tagsData = currency.models.TagsModel.objects.filter(type=1).order_by("?")[0:20]
            categoryList = currency.models.CategoryModel.objects.filter(type=1)
            articleData = currency.models.ArticleModel.objects.filter(is_recommend=False).order_by("-aid")
            totalCount = articleData.count()
            
            if articleData.count() > 0:
                hotData = articleData.order_by("-click_count")[0:3]
                firstData = articleData[0]
                firstPicData = getDeafulatPic(firstData.content).replace("blog","backblog")
                if articleData.count() >= 1:
                    articleData = articleData[1:]
                try:
                    pageNum = int(request.GET.get("page", 1))
                except Exception as e:
                    errorLogger(e)
                    pageNum = 1
                paginator = Paginator(articleData, 12)
                # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
                if pageNum < 0:
                    pageNum = 1
                if pageNum > paginator.num_pages:
                    pageNum = paginator.num_pages
                # 分页器获得当前页面的数据内容
                articleList = paginator.page(pageNum)
                articleResult = []
                for eveData in articleList:
                    picUrl = getDeafulatPic(eveData.content)
                    articleResult.append((eveData,picUrl.replace("blog","backblog")))
                hotList = []
                for eveHotData in hotData:
                    picUrl = getDeafulatPic(eveHotData.content)
                    hotList.append((eveHotData,picUrl.replace("blog","backblog")))
                if pageNum == 1:
                    pageTitle = "博客首页"
                else:
                    pageTitle = "第%d页"%(pageNum)
            else:
                noData = True
            return render(request, "blog/%s/%s" % (information.getValue("templatesBlogName"), "list.html"), locals())
        else:
            return redirect("/sorry")
    except Exception as e:
        print(e)
        errorLogger(e)
        request.session["errorNumber"] = "100004"
        return redirect("/wrong")

@cache_page(60 * 15, key_prefix="blogList")
def blogList(request):
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

            # 头部名人名言
            sentenceData = Sentence()
            (sentence, author) = sentenceData.getOneSentence()
            sentence = sentence[0:-1]

            
            articleData = currency.models.ArticleModel.objects.filter(is_recommend=False).order_by("-aid")
            totalCount = articleData.count()
            tagsData = currency.models.TagsModel.objects.filter(type=1).order_by("?")[0:20]
            categoryList = currency.models.CategoryModel.objects.filter(type=1)

            searchData = request.GET.get("search",None)

            if searchData:
                tempList = []
                for eveArticle in articleData:
                    tempList.append((eveArticle.title,filterTags(eveArticle.content),str(eveArticle.aid)))
                searchHandle = SearchArticleHandle(tempList)
                articleAidData = searchHandle.getResult(searchData)
                searchArticleData = []
                for eveAid in articleAidData:
                    searchArticleData.append(articleData.get(aid=eveAid))

                pageNum = 1
                if len(searchArticleData) > 0:
                    hotData = articleData.order_by("-click_count")[0:3]
                    firstData = searchArticleData[0]
                    firstPicData = getDeafulatPic(firstData.content)
                    if len(articleData) >= 1:
                        articleData = searchArticleData[1:]
                    else:
                        articleData = []
                    try:
                        pageNum = int(request.GET.get("page", 1))
                    except Exception as e:
                        errorLogger(e)
                    paginator = Paginator(articleData, 12)
                    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
                    if pageNum < 0:
                        pageNum = 1
                    if pageNum > paginator.num_pages:
                        pageNum = paginator.num_pages
                    # 分页器获得当前页面的数据内容
                    articleList = paginator.page(pageNum)
                    articleResult = []

                    for eveData in articleList:
                        picUrl = getDeafulatPic(eveData.content)
                        articleResult.append((eveData, picUrl))

                    hotList = []
                    for eveHotData in hotData:
                        picUrl = getDeafulatPic(eveHotData.content)
                        hotList.append((eveHotData, picUrl))
                else:
                    noData = True


                pageTempTitle = searchData + "搜索结果"

                if pageNum == 1:
                    pageTitle = pageTempTitle
                else:
                    pageTitle = "第%d页 - %s" % (pageNum, pageTempTitle)
            else:
                category = request.GET.get("cate",None)
                tag = request.GET.get("tag",None)
                categoryMainData = None
                tagMainData = None
                if category:
                    categoryMainData = currency.models.CategoryModel.objects.get(cid=category)
                    articleData = articleData.filter(category=categoryMainData,is_recommend=False).order_by("-aid")
                elif tag:
                    tagMainData = currency.models.TagsModel.objects.get(tid=tag)
                    articleData = articleData.filter(tag=tagMainData).order_by("-aid")


                pageNum = 1
                if articleData.count() > 0:
                    hotData = articleData.order_by("-click_count")[0:5]
                    firstData = articleData[0]
                    firstPicData = getDeafulatPic(firstData.content).replace("blog","backblog")
                    if articleData.count() >= 1:
                        articleData = articleData[1:]
                    else:
                        articleData = []
                    try:
                        pageNum = int(request.GET.get("page", 1))
                    except Exception as e:
                        errorLogger(e)
                    paginator = Paginator(articleData, 12)
                    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
                    if pageNum < 0:
                        pageNum = 1
                    if pageNum > paginator.num_pages:
                        pageNum = paginator.num_pages
                    # 分页器获得当前页面的数据内容
                    articleList = paginator.page(pageNum)
                    articleResult = []

                    for eveData in articleList:
                        picUrl = getDeafulatPic(eveData.content)
                        articleResult.append((eveData, picUrl.replace("blog","backblog")))

                    hotList = []
                    for eveHotData in hotData:
                        picUrl = getDeafulatPic(eveHotData.content)
                        hotList.append((eveHotData, picUrl.replace("blog","backblog")))
                else:
                    noData = True

                if categoryMainData:
                    pageTempTitle = categoryMainData.name
                elif categoryMainData:
                    pageTempTitle = tagMainData.name
                else:
                    pageTempTitle = "全部博文"

                if pageNum == 1:
                    pageTitle = pageTempTitle
                else:
                    pageTitle = "第%d页 - %s" % (pageNum,pageTempTitle)
            return render(request, "blog/%s/%s" % (information.getValue("templatesBlogName"), "list.html"), locals())
        else:
            return redirect("/sorry")
    except Exception as e:
        print(e)
        errorLogger(e)
        request.session["errorNumber"] = "100004"
        return redirect("/wrong")

@csrf_exempt
@cache_page(60 * 15, key_prefix="blogArticle")
def blogArticle(request):
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

            # 头部名人名言
            sentenceData = Sentence()
            (sentence, author) = sentenceData.getOneSentence()
            sentence = sentence[0:-1]

            tagsData = currency.models.TagsModel.objects.filter(type=1).order_by("?")[0:20]
            categoryList = currency.models.CategoryModel.objects.filter(type=1)

            aidData = request.GET.get("aid")

            articleData = currency.models.ArticleModel.objects.get(aid=aidData)
            if not articleData.is_recommend:
                clickCount = int(articleData.click_count) + 1
                currency.models.ArticleModel.objects.filter(aid=aidData).update(click_count = clickCount)

                articleListTemp = currency.models.ArticleModel.objects.filter(is_recommend=False)
                articleList = articleListTemp.order_by("-aid")
                totalCount = articleList.count()
                # recommend = RecommendedHandle(numCount=5)
                # otherArticle = []
                # for eveArticle in articleList:
                #     if str(aidData) == str(eveArticle.aid):
                #         articleData = eveArticle
                #     else:
                #         otherArticle.append((eveArticle.aid,"%s,%s,%s"%(eveArticle.title,eveArticle.category.name,eveArticle.desc)))

                # recommendList = recommend.getArticleList("%s,%s,%s"%(articleData.title,articleData.category.name,articleData.desc),otherArticle)
                # recommendArticle = []
                # for eveArticle in recommendList:
                #     tempArticle = currency.models.ArticleModel.objects.get(aid=eveArticle)
                #     recommendArticle.append((tempArticle,getDeafulatPic(tempArticle.content).replace("blog","backblog")))

                recommendArticleData = articleListTemp.order_by("-click_count")[0:3]
                recommendArticle = []
                for eveHotData in recommendArticleData:
                    picUrl = getDeafulatPic(eveHotData.content)
                    recommendArticle.append((eveHotData, picUrl.replace("blog","backblog")))

                loginId = isLoginTrue(request)
                totalUser = usercenter.models.UserModel.objects.all()
                try:
                    isLogin = True
                    userId = loginId[2]
                    userData = totalUser.get(uid=userId)
                except Exception as e:
                    errorLogger(e)
                    isLogin = False

                if request.method == "POST":
                    username = request.POST.get("name")
                    email = request.POST.get("email")
                    comment = request.POST.get("comment")

                    comment = filterTags(comment)
                    spamData = SpamHandle(comment).getSpam()


                    '''
                    cid = models.AutoField(primary_key=True)
                    content = models.TextField(verbose_name="评论内容")
                    date_publish = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
                    username = models.CharField(max_length=50, verbose_name="用户")
                    usertype = models.IntegerField(default=0, verbose_name="用户类型")
                    qq = models.CharField(max_length=13, blank=True, null=True, verbose_name="QQ号")
                    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name="电话号")
                    pid = models.ForeignKey('self', blank=True, null=True, verbose_name="父级评论")
                    is_recommend = models.BooleanField(default=True, verbose_name="是否显示")
                    watched = models.BooleanField(default=True, verbose_name="是否查看")
                    email = models.CharField(max_length=50, verbose_name="邮箱")
                    article = models.CharField(max_length=50, verbose_name="文章")
                    '''


                    if spamData:
                        try:
                            username = userData.username
                            email = userData.email
                            typeData = 1
                        except:
                            typeData = 0

                        # 登录用户的typeData是1，否则是0

                        currency.models.CommentsModel.objects.create(
                            username = username,
                            email = email,
                            content = comment,
                            is_recommend = False,
                            watched = False,
                            article_title = articleData.title,
                            article=articleData,
                            usertype = typeData,
                        )
                        stateData = "留言成功，我会尽快审核，给您反馈！感谢您的支持哦！"
                    else:
                        stateData = "系统判断，您的信息可能是垃圾信息,维护网络信息整洁是我们每个公民的义务！请您重新发送！"

                commenData = currency.models.CommentsModel.objects.filter(article=aidData, is_recommend=False).order_by("-cid")
                comm = []
                tempHave = []
                for eveComment in commenData:
                    if eveComment.pid:
                        if eveComment.pid.is_recommend:
                            if eveComment.pid.cid not in tempHave:
                                if eveComment.usertype == 1:
                                    comm.append((eveComment,totalUser.get(username=eveComment.username).photo))
                                else:
                                    comm.append((eveComment,"/files/userFace/1.jpg"))
                                tempHave.append(eveComment.pid.cid)
                    else:
                        if eveComment.cid not in tempHave:
                            if eveComment.usertype == 1:
                                comm.append((eveComment,totalUser.get(username=eveComment.username).photo))
                            else:
                                comm.append((eveComment,"/files/userFace/1.jpg"))

                return render(request, "blog/%s/%s" % (information.getValue("templatesBlogName"), "content.html"), locals())
            else:
                request.session["errorNumber"] = "100009"
                return redirect("/wrong")
        else:
            return redirect("/sorry")
    except Exception as e:
        errorLogger(e)
        request.session["errorNumber"] = "100004"
        return redirect("/wrong")


