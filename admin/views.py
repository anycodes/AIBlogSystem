from django.shortcuts import render
from django.core.paginator import *
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import redirect

from BlogSystem.information import Information
from currency.views import webLogger, ipCounter, errorLogger, isLoginTrue, filterTags
from artificialIntelligence.Article import ArticleHandle
from tools.everydaySentence.Sentence import Sentence

import currency.models
import album.models
import usercenter.models
import resume.models
import video.models

import BlogSystem.settings
import currency.views

import random
import time
import os
import re
import requests
from lxml import etree

import collections

# Create your views here.

def getBilibiliData(avNumber):
    urlData = "https://www.bilibili.com/video/av" + avNumber.strip()
    pageSource = requests.get(urlData).content.decode("utf-8")
    videoUrl = "".join(re.findall('src="(.*?)"',"".join(etree.HTML(pageSource).xpath('//*[@id="link2"]/@value'))))
    title = "".join(etree.HTML(pageSource).xpath('//*[@id="viewbox_report"]/h1/span/text()'))
    return (videoUrl, title)


def adminNavigation(navId):
    '''
    Admin的导航栏，是一个大的Dict
    :param navId: navID是传入的标识，用作active的判定
    :return: 返回带有Active的导航字典
    '''
    nav = collections.OrderedDict()
    nav["article"] = {
            "name": "文章管理",
            "icon": "ti-align-justify",
            "isFinal": False,
            "active": "",
            "nextDir": {
                "addArticle": {
                    "name": "新增文章",
                    "icon": "ti-plus",
                    "isFinal": True,
                    "nextDir": {}
                },
                "viewArticle": {
                    "name": "查看文章",
                    "icon": "ti-view-list",
                    "isFinal": True,
                    "nextDir": {}
                },
            }
        }
    nav["category"] = {
            "name": "分类管理",
            "icon": "ti-list",
            "isFinal": False,
            "active": "",
            "nextDir": {
                "addCategory": {
                    "name": "新增分类",
                    "icon": "ti-plus",
                    "isFinal": True,
                    "nextDir": {}
                },
                "viewCategory": {
                    "name": "查看分类",
                    "icon": "ti-view-list",
                    "isFinal": True,
                    "nextDir": {}
                },
            }
        }
    nav["tag"] = {
            "name": "标签管理",
            "icon": "ti-tag",
            "isFinal": False,
            "active": "",
            "nextDir": {
                "addTag": {
                    "name": "新增标签",
                    "icon": "ti-plus",
                    "isFinal": True,
                    "nextDir": {}
                },
                "viewTag": {
                    "name": "查看标签",
                    "icon": "ti-view-list",
                    "isFinal": True,
                    "nextDir": {}
                },
            }
        }
    nav["comments"] = {
            "name": "留言管理",
            "icon": "ti-pencil-alt",
            "isFinal": True,
            "active": "",
            "nextDir": {
            }
        }
    nav["photo"] = {
            "name": "相册中心",
            "icon": "ti-instagram",
            "isFinal": False,
            "active": "",
            "nextDir": {
                "uploadPhoto": {
                    "name": "上传图片",
                    "icon": "ti-upload",
                    "isFinal": True,
                    "nextDir": {}
                },
                "viewPhoto": {
                    "name": "图片列表",
                    "icon": "ti-view-list",
                    "isFinal": True,
                    "nextDir": {}
                },
            }
        }
    nav["file"] = {
            "name": "文件管理",
            "icon": "ti-harddrives",
            "isFinal": False,
            "active": "",
            "nextDir": {
                "addFile": {
                    "name": "上传文件",
                    "icon": "ti-upload",
                    "isFinal": True,
                    "nextDir": {}
                },
                "viewFile": {
                    "name": "查看文件",
                    "icon": "ti-view-list",
                    "isFinal": True,
                    "nextDir": {}
                },
            }
        }
    nav["video"] = {
        "name": "视频管理",
        "icon": "ti-video-clapper",
        "isFinal": False,
        "active": "",
        "nextDir": {
            "addVideo": {
                "name": "添加视频",
                "icon": "ti-upload",
                "isFinal": True,
                "nextDir": {}
            },
            "viewVideo": {
                "name": "查看视频",
                "icon": "ti-view-list",
                "isFinal": True,
                "nextDir": {}
            },
        }
    }
    nav["user"] = {
            "name": "用户列表",
            "icon": "ti-user",
            "isFinal": False,
            "active": "",
            "nextDir": {
                "addUser": {
                    "name": "新增用户",
                    "icon": "ti-plus",
                    "isFinal": True,
                    "nextDir": {}
                },
                "viewUser": {
                    "name": "用户列表",
                    "icon": "ti-view-list",
                    "isFinal": True,
                    "nextDir": {}
                },
            }
        }
    nav["resume"] = {
            "name": "简历中心",
            "icon": "ti-file",
            "isFinal": False,
            "active": "",
            "nextDir": {
                "addResume": {
                    "name": "新增简历",
                    "icon": "ti-plus",
                    "isFinal": True,
                    "nextDir": {}
                },
                "viewResume": {
                    "name": "简历列表",
                    "icon": "ti-view-list",
                    "isFinal": True,
                    "nextDir": {}
                },
            }
        }
    # nav["show"] = {
    #         "name": "插件中心",
    #         "icon": "ti-desktop",
    #         "isFinal": False,
    #         "active": "",
    #         "nextDir": {
    #             "timeline": {
    #                 "name": "记录时光",
    #                 "icon": "ti-time",
    #                 "isFinal": True,
    #                 "nextDir": {}
    #             },
    #         }
    #     }
    nav["setting"] = {
            "name": "系统设置",
            "icon": "ti-settings",
            "isFinal": False,
            "active": "",
            "nextDir": {
                "webSetting": {
                    "name": "整体设置",
                    "icon": "ti-panel",
                    "isFinal": True,
                    "nextDir": {}
                },
                "mysqlSetting": {
                    "name": "数据库设置",
                    "icon": "ti-pie-chart",
                    "isFinal": True,
                    "nextDir": {}
                },
                "emailSetting": {
                    "name": "邮箱设置",
                    "icon": "ti-comment",
                    "isFinal": True,
                    "nextDir": {}
                },
                "otherSetting": {
                    "name": "其他设置",
                    "icon": "ti-mouse-alt",
                    "isFinal": True,
                    "nextDir": {}
                },
            }
        }
    # 根据navID修改相应的active
    nav[navId]["active"] = "active"
    return nav


@csrf_exempt
def adminArticleAdd(request):
    '''
    网站文章添加页面
    :param request:
    :return:
    '''
    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("article")
    nextNavBar = navbar["article"]["nextDir"]
    pageTitle = "添加文章"

    # 获得文章的分类列表/标签列表
    categoryList = currency.models.CategoryModel.objects.filter(type="1").order_by("-cid")
    tagList = currency.models.TagsModel.objects.filter(type="1")

    # 获得aid参数，如果有aid的参数，代表这是查看功能
    aidData = request.GET.get("aid")

    # 判断查看文章的上一层路径，此处不可以用refer_http，因为中间经历过跳转
    # 主要是判断来源是分类归类中/标签归类中来源，handleUrl是handle页面跳转URL
    tempUrlData = str(request.get_full_path()).replace("aid=%s" % (aidData), "").replace("?&", "?")
    if "cid" in tempUrlData:
        handleUrl = tempUrlData.replace("addArticle", "addCategory")
    elif "tid" in tempUrlData:
        handleUrl = tempUrlData.replace("addArticle", "addTag")
    else:
        handleUrl = "viewArticle?sort=date&snum=1"

    if aidData:
        try:
            # 如果有aidData参数，前台进行数据显示的View信息
            articleDataView = currency.models.ArticleModel.objects.get(aid=int(aidData))
            articleTitleView = articleDataView.title
            articleContentView = articleDataView.content
            articleDescView = articleDataView.desc
            articleCategoryView = articleDataView.category
            articlePublishView = articleDataView.is_recommend
            articleTagsView = articleDataView.tag.all()
            articleTypeView = articleDataView.type
            tagData = []
            pageTitle = "修改文章"
            for eveTagData in articleTagsView:
                tagData.append(eveTagData.name)
            articleTagsView = ",".join(tagData)
        except Exception as e:
            errorLogger(e)
            saveToDB = ("danger", "该数据已不再数据库中，查询失败！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                          locals())

    # 如果请求模式是post，则表示提交了数据
    if request.method == "POST":

        # 获取提交的数据
        articleTitle = request.POST.get("title")
        articleContent = request.POST.get("content")
        articleDesc = request.POST.get("description")
        articleCategory = request.POST.get("category")
        articlePublish = request.POST.get("publish")
        articleTags = request.POST.get("tags")
        articleType = request.POST.get("type")

        # 如果非法提交了articleTitle,articleContent,articlePublish和articleCategory，则发出警告
        if not articleTitle or not articleContent or not articlePublish or not articleCategory:
            saveToDB = ("warning", "文章标题，文章内容，是否发布以及分类等信息是必选项！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "articleAdd.html"),
                          locals())

        # 对articleTags，articleDesc进行处理，主要是通过AI功能实现自动摘要和自动关键词
        if articleTags:
            if "," in articleTags:
                articleTags = articleTags.split(",")
            else:
                articleTags = [articleTags, ]
        if not articleDesc or not articleTags:
            if len(articleContent) < 200:
                if not articleDesc:
                    articleDesc = ""
                if not articleTags:
                    articleTags = ""
            else:
                aiArticle = ArticleHandle(filterTags(articleContent))
                if not articleDesc:
                    articleDesc = aiArticle.getAbstract()
                if not articleTags:
                    articleTags = aiArticle.getKeywords()

        # 对前台传递的articlePublish进行单独的处理
        if articlePublish == "true":
            articlePublish = True  # 草稿
        else:
            articlePublish = False # 发布

        # 如果有cidData，则表示这个是查看并且修改
        if aidData:
            try:
                '''
                    aid = models.AutoField(primary_key=True)
                    title = models.CharField(max_length=50, verbose_name="文章标题")
                    desc = models.TextField(verbose_name="文章描述")
                    content = models.TextField(verbose_name="文章内容")
                    click_count = models.IntegerField(default=0, verbose_name="点击次数")
                    date_publish = models.DateTimeField(auto_created=True,auto_now_add=True,verbose_name="发布时间")
                    user = models.CharField(max_length=50, verbose_name="用户")
                    category = models.ForeignKey(CategoryModel, blank=True, null=True, verbose_name="分类")
                    tag = models.ManyToManyField(TagsModel, verbose_name="标签")
                    is_recommend = models.BooleanField(default=True, verbose_name="是否显示")
                    type = models.CharField(max_length=30, verbose_name="类型")
                    watched = models.BooleanField(default=True, verbose_name="是否查看")
                '''
                # 数据库升级
                articleDBModel = currency.models.ArticleModel.objects.filter(aid=int(aidData)).update(
                    title=articleTitle,
                    desc=articleDesc,
                    content=articleContent,
                    user=usercenter.models.UserModel.objects.get(uid=loginUid),
                    category=categoryList.get(cid=articleCategory),
                    type=articleType,
                    is_recommend=articlePublish
                )
                # 数据库升级之后，对tags（多对多关系的单独处理）
                articleDBModel = currency.models.ArticleModel.objects.get(aid=int(aidData))
                articleDBModel.tag.clear()
                if articleTags:
                    for eveTag in articleTags:
                        if eveTag:
                            # 判断tags是否存在，不出异常表示存在，出现异常表示不存在，则新建
                            try:
                                tag_obj = currency.models.TagsModel.objects.get(name=eveTag, type="1")
                            except Exception as e:
                                tag_obj = currency.models.TagsModel.objects.create(name=eveTag, type="1",
                                                                                   unique="%s-%s" % (
                                                                                   str(eveTag), str("1")))
                            articleDBModel.tag.add(tag_obj)
                saveToDB = ("success", "修改成功！为您跳转到列表页面！")
                try:
                    countData = currency.models.ArticleModel.objects.filter(category=categoryList.get(cid=articleCategory)).count()
                    categoryList.filter(cid=articleCategory).update(count = countData)
                    print(countData)
                except Exception as e:
                    print(e)
                    errorLogger(e)
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "修改失败，请检查是否之前已经添加过类似的内容。")
        else:
            # 否则是新建数据
            try:
                '''
                    cid = models.AutoField(primary_key=True)
                    name = models.CharField(max_length=30, verbose_name="名称")
                    index = models.IntegerField(default=999, verbose_name="排序")
                    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
                    remark = models.CharField(max_length=150, verbose_name="备注说明")
                    type = models.CharField(max_length=30, verbose_name="类型")
                    unique = models.CharField(max_length=150, unique=True, verbose_name="唯一性判断")
                '''
                # 新建数据在数据库中
                articleDBModel = currency.models.ArticleModel.objects.create(
                    title=articleTitle,
                    desc=articleDesc,
                    content=articleContent,
                    user=usercenter.models.UserModel.objects.get(uid=loginUid),
                    category=categoryList.get(cid=articleCategory),
                    type=articleType,
                    is_recommend=articlePublish
                )
                # 将tags信息存入到数据库
                articleDBModel.tag.clear()
                if articleTags:
                    for eveTag in articleTags:
                        if eveTag:
                            # 判断tags是否存在，不出异常表示存在，出现异常表示不存在，则新建
                            try:
                                tag_obj = currency.models.TagsModel.objects.get(name=eveTag, type="1")
                            except Exception as e:
                                tag_obj = currency.models.TagsModel.objects.create(name=eveTag, type="1",
                                                                                   unique="%s-%s" % (
                                                                                   str(eveTag), str("1")))
                            articleDBModel.tag.add(tag_obj)
                saveToDB = ("success", "添加成功！为您跳转到列表页面！")


                try:
                    countData = currency.models.ArticleModel.objects.filter(category=categoryList.get(cid=articleCategory)).count()
                    categoryList.filter(cid=articleCategory).update(count = countData)
                    print(countData)
                except Exception as e:
                    print(e)
                    errorLogger(e)

                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "添加失败，请检查是否之前已经添加过类似的内容。")



    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "articleAdd.html"), locals())


def adminArticleView(request):
    '''
    文章列表查看功能，主要包括文章列表查看，和文章删除功能
    :param request:
    :return:
    '''
    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("article")
    nextNavBar = navbar["article"]["nextDir"]
    pageTitle = "文章列表"

    # 获取整体url
    pageUrl = request.get_raw_uri()

    # 此处进行删除操作
    if request.GET.get("dele"):
        # 如果请求的参数仲有dele和aid，则进行删除操作
        deleAidData = request.GET.get("aid")
        if deleAidData:
            try:
                deleResult = currency.models.ArticleModel.objects.filter(aid=int(deleAidData)).delete()
                if deleResult[0] == 0:
                    saveToDB = ("danger", "删除失败！未发现该条数据！")
                else:
                    saveToDB = ("success", "删除成功！为您刷新列表页面！")
            except Exception as e:
                errorLogger(e)
                saveToDB = ("danger", "删除失败，请检查数据是否存在！")
        else:
            saveToDB = ("danger", "删除失败，请检查参数是否正确！")

        # 删除之后的数据跳转操作
        urlList = []
        pageNum = request.GET.get("page")
        sortNum = request.GET.get("snum")
        sortType = request.GET.get("sort")
        if pageNum:
            urlList.append("page=" + pageNum)
        if sortNum:
            urlList.append("snum=" + sortNum)
        if sortType:
            urlList.append("sort=" + sortType)
        newUrl = "&".join(urlList)

        handleUrl = "viewArticle?" + newUrl
        return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                      locals())

    # 此处从数据库中提取数据
    articleAll = currency.models.ArticleModel.objects.all().order_by("-aid")

    # 进行数据排序，根据前端传递过来的参数，可能有ID，name，type，sort以及date等五种排序，其中ID排序为默认排序
    # 接受数据，其中sortNum是顺序方向，1表示从大到小，其他表示从小到大
    sortType = request.GET.get("sort")
    sortNum = request.GET.get("snum", "1")

    # 这里是设置默认排序为ID，并且提取出defaultString便于前端使用，保持前后url的一致性
    if sortType:
        defaultString = "sort=%s&snum=%s" % (sortType, sortNum)
    else:
        defaultString = ""
        sortType = "id"
    # 这里是进行排序
    if sortType == "title":
        if sortNum == "1":
            articleAll = articleAll.order_by("-title")
        else:
            articleAll = articleAll.order_by("title")
    elif sortType == "click_count":
        if sortNum == "1":
            articleAll = articleAll.order_by("-click_count")
        else:
            articleAll = articleAll.order_by("click_count")
    elif sortType == "date_publish" or sortType == "date":
        if sortNum == "1":
            articleAll = articleAll.order_by("-date_publish")
        else:
            articleAll = articleAll.order_by("date_publish")
    elif sortType == "category":
        if sortNum == "1":
            articleAll = articleAll.order_by("-category")
        else:
            articleAll = articleAll.order_by("category")
    else:
        articleAll = articleAll.order_by("-aid")

    # 对页码进行处理，并进行分页
    # 页码只接受传递进来的数字类型，默认是1
    try:
        pageNum = int(request.GET.get("page", 1))
    except Exception as e:
        errorLogger(e)
        pageNum = 1
    # 进行分页，此处为分页器分页，默认每页5条数据
    paginator = Paginator(articleAll, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    articleList = paginator.page(pageNum)

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "articleView.html"), locals())


@csrf_exempt
def adminCategoryAdd(request):
    '''
    添加分类信息页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("category")
    nextNavBar = navbar["category"]["nextDir"]
    pageTitle = "添加分类"

    handleUrl = "viewCategory?sort=date&snum=1"

    # 如果有cid的参数，代表这是查看功能
    cidData = request.GET.get("cid")
    if cidData:
        try:
            categoryDataView = currency.models.CategoryModel.objects.get(cid=int(cidData))
            categoryNameView = categoryDataView.name
            categoryTypeView = categoryDataView.type
            categorySortView = categoryDataView.index
            categoryRemarkView = categoryDataView.remark
            pageTitle = "修改分类"

            if categoryTypeView == "1":
                # 此功能用于添加标签查看时，下部分的文章列表功能
                # 此处从数据库中提取数据
                articleAll = currency.models.ArticleModel.objects.filter(category=categoryDataView).order_by("-aid")

                # 进行数据排序，根据前端传递过来的参数，可能有ID，name，type，sort以及date等五种排序，其中ID排序为默认排序
                # 接受数据，其中sortNum是顺序方向，1表示从大到小，其他表示从小到大
                sortType = request.GET.get("sort")
                sortNum = request.GET.get("snum", "1")

                # 对页码进行处理，并进行分页
                # 页码只接受传递进来的数字类型，默认是1
                try:
                    pageNum = int(request.GET.get("page", 1))
                except Exception as e:
                    errorLogger(e)
                    pageNum = 1
                # 进行分页，此处为分页器分页，默认每页5条数据
                paginator = Paginator(articleAll, 10)
                # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
                if pageNum < 0:
                    pageNum = 1
                if pageNum > paginator.num_pages:
                    pageNum = paginator.num_pages
                # 分页器获得当前页面的数据内容
                articleList = paginator.page(pageNum)
            else:
                # 此处从数据库中提取数据
                photoAll = album.models.ImagesModel.objects.filter(album=categoryDataView).order_by("-iid")

                # 对页码进行处理，并进行分页
                # 页码只接受传递进来的数字类型，默认是1
                try:
                    pageNum = int(request.GET.get("page", 1))
                except Exception as e:
                    errorLogger(e)
                    pageNum = 1
                # 进行分页，此处为分页器分页，默认每页5条数据
                paginator = Paginator(photoAll, 10)
                # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
                if pageNum < 0:
                    pageNum = 1
                if pageNum > paginator.num_pages:
                    pageNum = paginator.num_pages
                # 分页器获得当前页面的数据内容
                photoList = paginator.page(pageNum)

        except Exception as e:
            errorLogger(e)
            print(e)
            saveToDB = ("danger", "该数据已不再数据库中，查询失败！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                          locals())

        # 用于标签查看时，列表功能发起删除指令的处理
        if request.GET.get("dele"):

            if categoryTypeView == "1":
                # 如果请求的参数仲有dele和cid，则进行删除操作
                deleAidData = request.GET.get("aid")
                if deleAidData:
                    try:
                        deleResult = currency.models.ArticleModel.objects.filter(aid=int(deleAidData)).delete()
                        if deleResult[0] == 0:
                            saveToDB = ("danger", "删除失败！未发现该条数据！")
                        else:
                            saveToDB = ("success", "删除成功！为您刷新列表页面！")
                    except Exception as e:
                        errorLogger(e)
                        saveToDB = ("danger", "删除失败，请检查数据是否存在！")
                else:
                    saveToDB = ("danger", "删除失败，请检查参数是否正确！")

                # 删除之后的数据跳转操作
                try:
                    handleUrl = request.META["HTTP_REFERER"]
                except Exception as e:
                    errorLogger(e)
                handleUrl = "addCategory?cid=" + cidData
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            else:
                if request.GET.get("dele"):
                    # 如果请求的参数仲有dele和aid，则进行删除操作
                    deleIidData = request.GET.get("iid")
                    if deleIidData:
                        try:
                            deleResult = album.models.ImagesModel.objects.filter(iid=int(deleIidData)).delete()
                            if deleResult[0] == 0:
                                saveToDB = ("danger", "删除失败！未发现该条数据！")
                            else:
                                saveToDB = ("success", "删除成功！为您刷新列表页面！")
                        except Exception as e:
                            errorLogger(e)
                            saveToDB = ("danger", "删除失败，请检查数据是否存在！")
                    else:
                        saveToDB = ("danger", "删除失败，请检查参数是否正确！")

                    # 删除之后的数据跳转操作
                    try:
                        handleUrl = request.META["HTTP_REFERER"]
                    except Exception as e:
                        errorLogger(e)
                    handleUrl = "addCategory?cid=" + cidData
                    return render(request,
                                  "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                                  locals())

    # 如果请求模式是post，则表示提交了数据
    if request.method == "POST":

        # 获取提交的数据
        categoryName = request.POST.get("name")
        categoryType = request.POST.get("type")
        categorySort = request.POST.get("sort")
        categoryRemark = request.POST.get("remark")

        # 给categorySort变量赋予默认值999
        if not categorySort:
            categorySort = 999

        # 如果非法提交了categoryName和categoryType，则发出警告
        if not categoryName or not categoryType:
            saveToDB = ("warning", "分类名称和分类类型是必选内容，必须填写！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "categoryAdd.html"),
                          locals())

        # 如果有cidData，则表示这个是查看并且修改
        if cidData:
            try:
                '''
                    cid = models.AutoField(primary_key=True)
                    name = models.CharField(max_length=30, verbose_name="名称")
                    index = models.IntegerField(default=999, verbose_name="排序")
                    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
                    remark = models.CharField(max_length=150, verbose_name="备注说明")
                    type = models.CharField(max_length=30, verbose_name="类型")
                    unique = models.CharField(max_length=150, unique=True, verbose_name="唯一性判断")
                '''
                # 更新数据
                categoryDBModel = currency.models.CategoryModel.objects.filter(cid=int(cidData)).update(
                    name=categoryName,
                    type=categoryType,
                    index=categorySort,
                    remark=categoryRemark,
                    unique="%s-%s" % (str(categoryName), str(categoryType)),
                )
                saveToDB = ("success", "修改成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "修改失败，请检查是否之前已经添加过类似的内容。")

        else:
            # 否则是新建数据
            try:
                '''
                    cid = models.AutoField(primary_key=True)
                    name = models.CharField(max_length=30, verbose_name="名称")
                    index = models.IntegerField(default=999, verbose_name="排序")
                    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
                    remark = models.CharField(max_length=150, verbose_name="备注说明")
                    type = models.CharField(max_length=30, verbose_name="类型")
                    unique = models.CharField(max_length=150, unique=True, verbose_name="唯一性判断")
                '''
                # 新建数据
                categoryDBModel = currency.models.CategoryModel.objects.create(
                    name=categoryName,
                    type=categoryType,
                    index=categorySort,
                    remark=categoryRemark,
                    unique="%s-%s" % (str(categoryName), str(categoryType)),
                )
                saveToDB = ("success", "添加成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "添加失败，请检查是否之前已经添加过类似的内容。")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "categoryAdd.html"), locals())


def adminCategoryView(request):
    '''
    分类查看页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("category")
    nextNavBar = navbar["category"]["nextDir"]
    pageTitle = "分类列表"

    # 获取整体url
    pageUrl = request.get_raw_uri()

    # 此处进行删除操作
    if request.GET.get("dele"):
        # 如果请求的参数仲有dele和cid，则进行删除操作
        deleCidData = request.GET.get("cid")
        if deleCidData:
            try:
                deleResult = currency.models.CategoryModel.objects.filter(cid=int(deleCidData)).delete()
                if deleResult[0] == 0:
                    saveToDB = ("danger", "删除失败！未发现该条数据！")
                else:
                    saveToDB = ("success", "删除成功！为您刷新列表页面！")
            except Exception as e:
                errorLogger(e)
                saveToDB = ("danger", "删除失败，请检查数据是否存在！")
        else:
            saveToDB = ("danger", "删除失败，请检查参数是否正确！")

        # 删除之后的数据跳转操作
        urlList = []
        pageNum = request.GET.get("page")
        sortNum = request.GET.get("snum")
        sortType = request.GET.get("sort")
        if pageNum:
            urlList.append("page=" + pageNum)
        if sortNum:
            urlList.append("snum=" + sortNum)
        if sortType:
            urlList.append("sort=" + sortType)
        newUrl = "&".join(urlList)

        handleUrl = "viewCategory?" + newUrl
        return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                      locals())

    # 此处从数据库中提取数据
    categoryAll = currency.models.CategoryModel.objects.all().order_by("-cid")

    # 进行数据排序，根据前端传递过来的参数，可能有ID，name，type，sort以及date等五种排序，其中ID排序为默认排序
    # 接受数据，其中sortNum是顺序方向，1表示从大到小，其他表示从小到大
    sortType = request.GET.get("sort")
    sortNum = request.GET.get("snum", "1")

    # 这里是设置默认排序为ID，并且提取出defaultString便于前端使用，保持前后url的一致性
    if sortType:
        defaultString = "sort=%s&snum=%s" % (sortType, sortNum)
    else:
        defaultString = ""
        sortType = "id"
    # 这里是进行排序
    if sortType == "name":
        if sortNum == "1":
            categoryAll = categoryAll.order_by("-name")
        else:
            categoryAll = categoryAll.order_by("name")
    elif sortType == "type":
        if sortNum == "1":
            categoryAll = categoryAll.order_by("-type")
        else:
            categoryAll = categoryAll.order_by("type")
    elif sortType == "index":
        if sortNum == "1":
            categoryAll = categoryAll.order_by("-index")
        else:
            categoryAll = categoryAll.order_by("index")
    elif sortType == "date":
        if sortNum == "1":
            categoryAll = categoryAll.order_by("-date")
        else:
            categoryAll = categoryAll.order_by("date")
    else:
        categoryAll = categoryAll.order_by("-cid")

    # 用于数据的前端使用，由于前端想要用count这个参数，所以此处需要单独二次处理
    categoryListData = []
    for eveData in categoryAll:
        if eveData.type == "1":
            count = currency.models.ArticleModel.objects.filter(category=eveData).count()
        else:
            count = album.models.ImagesModel.objects.filter(album=eveData).count()
        categoryListData.append(
            {
                "cid": eveData.cid,
                "name": eveData.name,
                "index": eveData.index,
                "date": eveData.date,
                "type": eveData.type,
                "count": count,
            }
        )

    # 对页码进行处理，并进行分页
    # 页码只接受传递进来的数字类型，默认是1
    try:
        pageNum = int(request.GET.get("page", 1))
    except Exception as e:
        errorLogger(e)
        pageNum = 1
    # 进行分页，此处为分页器分页，默认每页5条数据
    paginator = Paginator(categoryListData, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    categoryList = paginator.page(pageNum)

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "categoryView.html"), locals())


@csrf_exempt
def adminTagAdd(request):
    '''
    标签添加页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("tag")
    nextNavBar = navbar["tag"]["nextDir"]
    pageTitle = "添加标签"

    handleUrl = "viewTag?sort=date&snum=1"

    # 如果有tid的参数，代表这是查看功能
    tidData = request.GET.get("tid")
    if tidData:
        try:
            tagDataView = currency.models.TagsModel.objects.get(tid=int(tidData))
            tagNameView = tagDataView.name
            tagTypeView = tagDataView.type
            tagRemarkView = tagDataView.remark
            pageTitle = "修改标签"

            if tagTypeView == "1":
                # 此功能用于添加标签查看时，下部分的文章列表功能
                # 此处从数据库中提取数据
                articleAll = currency.models.ArticleModel.objects.filter(tag=tagDataView).order_by("-aid")

                # 进行数据排序，根据前端传递过来的参数，可能有ID，name，type，sort以及date等五种排序，其中ID排序为默认排序
                # 接受数据，其中sortNum是顺序方向，1表示从大到小，其他表示从小到大
                sortType = request.GET.get("sort")
                sortNum = request.GET.get("snum", "1")

                # 对页码进行处理，并进行分页
                # 页码只接受传递进来的数字类型，默认是1
                try:
                    pageNum = int(request.GET.get("page", 1))
                except Exception as e:
                    errorLogger(e)
                    pageNum = 1
                # 进行分页，此处为分页器分页，默认每页5条数据
                paginator = Paginator(articleAll, 10)
                # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
                if pageNum < 0:
                    pageNum = 1
                if pageNum > paginator.num_pages:
                    pageNum = paginator.num_pages
                # 分页器获得当前页面的数据内容
                articleList = paginator.page(pageNum)
            else:
                # 此处从数据库中提取数据
                photoAll = album.models.ImagesModel.objects.filter(tag=tagDataView).order_by("iid")

                # 对页码进行处理，并进行分页
                # 页码只接受传递进来的数字类型，默认是1
                try:
                    pageNum = int(request.GET.get("page", 1))
                except Exception as e:
                    errorLogger(e)
                    pageNum = 1
                # 进行分页，此处为分页器分页，默认每页5条数据
                paginator = Paginator(photoAll, 10)
                # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
                if pageNum < 0:
                    pageNum = 1
                if pageNum > paginator.num_pages:
                    pageNum = paginator.num_pages
                # 分页器获得当前页面的数据内容
                photoList = paginator.page(pageNum)

        except Exception as e:
            errorLogger(e)
            saveToDB = ("danger", "该数据已不再数据库中，查询失败！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                          locals())

        # 用于标签查看时，列表功能发起删除指令的处理
        if request.GET.get("dele"):
            if tagTypeView == "1":
                # 如果请求的参数仲有dele和cid，则进行删除操作
                deleAidData = request.GET.get("aid")
                if deleAidData:
                    try:
                        deleResult = currency.models.ArticleModel.objects.filter(aid=int(deleAidData)).delete()
                        if deleResult[0] == 0:
                            saveToDB = ("danger", "删除失败！未发现该条数据！")
                        else:
                            saveToDB = ("success", "删除成功！为您刷新列表页面！")
                    except Exception as e:
                        errorLogger(e)
                        saveToDB = ("danger", "删除失败，请检查数据是否存在！")
                else:
                    saveToDB = ("danger", "删除失败，请检查参数是否正确！")

                # 删除之后的数据跳转操作
                try:
                    handleUrl = request.META["HTTP_REFERER"]
                except Exception as e:
                    errorLogger(e)
                handleUrl = "addTag?tid=" + tidData
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            elif tagTypeView == "2":
                pass
            else:
                if request.GET.get("dele"):
                    # 如果请求的参数仲有dele和aid，则进行删除操作
                    deleIidData = request.GET.get("iid")
                    if deleIidData:
                        try:
                            deleResult = album.models.ImagesModel.objects.filter(iid=int(deleIidData)).delete()
                            if deleResult[0] == 0:
                                saveToDB = ("danger", "删除失败！未发现该条数据！")
                            else:
                                saveToDB = ("success", "删除成功！为您刷新列表页面！")
                        except Exception as e:
                            errorLogger(e)
                            saveToDB = ("danger", "删除失败，请检查数据是否存在！")
                    else:
                        saveToDB = ("danger", "删除失败，请检查参数是否正确！")

                    # 删除之后的数据跳转操作
                    try:
                        handleUrl = request.META["HTTP_REFERER"]
                    except Exception as e:
                        errorLogger(e)
                    handleUrl = "addTag?tid=" + tidData
                    return render(request,
                                  "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                                  locals())

    # 如果请求模式是post，则表示提交了数据
    if request.method == "POST":

        # 获取提交的数据
        tagName = request.POST.get("name")
        tagType = request.POST.get("type")
        tagRemark = request.POST.get("remark")

        # 如果非法提交了tagName和tagType，则发出警告
        if not tagName or not tagType:
            saveToDB = ("warning", "标签名称和标签类型是必选内容，必须填写！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "tagAdd.html"),
                          locals())

        # 如果有tidData，则表示这个是查看并且修改
        if tidData:
            try:
                '''
                    cid = models.AutoField(primary_key=True)
                    name = models.CharField(max_length=30, verbose_name="名称")
                    index = models.IntegerField(default=999, verbose_name="排序")
                    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
                    remark = models.CharField(max_length=150, verbose_name="备注说明")
                    type = models.CharField(max_length=30, verbose_name="类型")
                    unique = models.CharField(max_length=150, unique=True, verbose_name="唯一性判断")
                '''
                # 数据库中更新数据
                tagDBModel = currency.models.TagsModel.objects.filter(tid=int(tidData)).update(
                    name=tagName,
                    type=tagType,
                    remark=tagRemark,
                    unique="%s-%s" % (str(tagName), str(tagType)),
                )
                saveToDB = ("success", "修改成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "修改失败，请检查是否之前已经添加过类似的内容。")

        else:
            # 否则是新建数据
            try:
                '''
                    tid = models.AutoField(primary_key=True)
                    name = models.CharField(max_length=30, verbose_name="标签名称")
                    remark = models.CharField(max_length=150, verbose_name="备注说明")
                    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
                    type = models.CharField(max_length=30, verbose_name="类型")
                    unique = models.CharField(max_length=150, unique=True, verbose_name="唯一性判断")
                '''
                # 数据库中新建数据
                tagDBModel = currency.models.TagsModel.objects.create(
                    name=tagName,
                    type=tagType,
                    remark=tagRemark,
                    unique="%s-%s" % (str(tagName), str(tagType)),
                )
                saveToDB = ("success", "添加成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "添加失败，请检查是否之前已经添加过类似的内容。")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "tagAdd.html"), locals())


def adminTagView(request):
    '''
    标签查看页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("tag")
    nextNavBar = navbar["tag"]["nextDir"]
    pageTitle = "标签列表"

    # 获取整体url
    pageUrl = request.get_raw_uri()

    # 此处进行删除操作
    if request.GET.get("dele"):
        # 如果请求的参数仲有dele和cid，则进行删除操作
        deleTidData = request.GET.get("tid")
        if deleTidData:
            try:
                deleResult = currency.models.TagsModel.objects.filter(tid=int(deleTidData)).delete()
                if deleResult[0] == 0:
                    saveToDB = ("danger", "删除失败！未发现该条数据！")
                else:
                    saveToDB = ("success", "删除成功！为您刷新列表页面！")
            except Exception as e:
                errorLogger(e)
                saveToDB = ("danger", "删除失败，请检查数据是否存在！")
        else:
            saveToDB = ("danger", "删除失败，请检查参数是否正确！")

        # 删除之后的数据跳转操作
        urlList = []
        pageNum = request.GET.get("page")
        sortNum = request.GET.get("snum")
        sortType = request.GET.get("sort")
        if pageNum:
            urlList.append("page=" + pageNum)
        if sortNum:
            urlList.append("snum=" + sortNum)
        if sortType:
            urlList.append("sort=" + sortType)
        newUrl = "&".join(urlList)

        handleUrl = "viewTag?" + newUrl
        return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                      locals())

    # 此处从数据库中提取数据
    tagAll = currency.models.TagsModel.objects.all().order_by("-tid")

    # 进行数据排序，根据前端传递过来的参数，可能有ID，name，type，sort以及date等五种排序，其中ID排序为默认排序
    # 接受数据，其中sortNum是顺序方向，1表示从大到小，其他表示从小到大
    sortType = request.GET.get("sort")
    sortNum = request.GET.get("snum", "1")

    # 这里是设置默认排序为ID，并且提取出defaultString便于前端使用，保持前后url的一致性
    if sortType:
        defaultString = "sort=%s&snum=%s" % (sortType, sortNum)
    else:
        defaultString = ""
        sortType = "id"
    # 这里是进行排序
    if sortType == "name":
        if sortNum == "1":
            tagAll = tagAll.order_by("-name")
        else:
            tagAll = tagAll.order_by("name")
    elif sortType == "type":
        if sortNum == "1":
            tagAll = tagAll.order_by("-type")
        else:
            tagAll = tagAll.order_by("type")
    elif sortType == "date":
        if sortNum == "1":
            tagAll = tagAll.order_by("-date")
        else:
            tagAll = tagAll.order_by("date")
    else:
        tagAll = tagAll.order_by("-tid")

    # 用于数据的前端使用，由于前端想要用count这个参数，所以此处需要单独二次处理
    tagListData = []
    for eveData in tagAll:
        if eveData.type == "1":
            count = currency.models.ArticleModel.objects.filter(tag=eveData).count()
        else:
            count = album.models.ImagesModel.objects.filter(tag=eveData).count()

        tagListData.append(
            {
                "tid": eveData.tid,
                "name": eveData.name,
                "date": eveData.date,
                "type": eveData.type,
                "count": count,
            }
        )

    # 对页码进行处理，并进行分页
    # 页码只接受传递进来的数字类型，默认是1
    try:
        pageNum = int(request.GET.get("page", 1))
    except Exception as e:
        errorLogger(e)
        pageNum = 1
    # 进行分页，此处为分页器分页，默认每页5条数据
    paginator = Paginator(tagListData, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    tagList = paginator.page(pageNum)

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "tagView.html"), locals())

@csrf_exempt
def adminCommentsAdd(request):
    '''
    评论查看页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
        # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("comments")
    nextNavBar = navbar["comments"]["nextDir"]
    pageTitle = "评论中心"

    handleUrl = "comments?sort=date&snum=1"

    try:

        userData = usercenter.models.UserModel.objects.get(uid=isLogin[2])

        # 获取整体url
        pageUrl = request.get_raw_uri()

        cidData = request.GET.get("cid")

        commentData = currency.models.CommentsModel.objects.filter(cid=cidData)
        commentData.update(
            watched = True,
        )
        commentData = commentData[0]
        articleData = commentData.article
        try:
            reCommentData = currency.models.CommentsModel.objects.get(pid=commentData)
        except:
            reCommentData = None

        if request.method == "POST":
            content = request.POST.get("content")
            if reCommentData:
                currency.models.CommentsModel.objects.filter(pid=commentData).update(
                    username=userData.username,
                    email=userData.email,
                    content=content,
                    is_recommend=True,
                    watched=True,
                    article_title=articleData.title,
                    article=articleData,
                    pid=commentData,
                    usertype = 1,
                )
                saveToDB = ("success", "修改成功！为您跳转到列表页面！")
            else:
                currency.models.CommentsModel.objects.create(
                    username=userData.username,
                    email=userData.email,
                    content=content,
                    is_recommend=True,
                    watched=True,
                    article_title=articleData.title,
                    article=articleData,
                    pid=commentData,
                    usertype = 1,
                )
                saveToDB = ("success", "回复成功！为您跳转到列表页面！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),locals())
    except Exception as e:
        print(e)
        saveToDB = ("danger", "文章已被删除")
        return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),locals())

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "commentAdd.html"), locals())


def adminComments(request):
    '''
    评论列表页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("comments")
    nextNavBar = navbar["comments"]["nextDir"]
    pageTitle = "评论中心"

    # 获取整体url
    pageUrl = request.get_raw_uri()

    # 此处进行删除操作
    if request.GET.get("dele"):
        # 如果请求的参数仲有dele和cid，则进行删除操作
        deleCidData = request.GET.get("cid")
        if deleCidData:
            try:
                deleResult = currency.models.CommentsModel.objects.filter(cid=int(deleCidData)).delete()
                if deleResult[0] == 0:
                    saveToDB = ("danger", "删除失败！未发现该条数据！")
                else:
                    saveToDB = ("success", "删除成功！为您刷新列表页面！")
            except Exception as e:
                errorLogger(e)
                saveToDB = ("danger", "删除失败，请检查数据是否存在！")
        else:
            saveToDB = ("danger", "删除失败，请检查参数是否正确！")

        # 删除之后的数据跳转操作
        urlList = []
        pageNum = request.GET.get("page")
        sortNum = request.GET.get("snum")
        sortType = request.GET.get("sort")
        if pageNum:
            urlList.append("page=" + pageNum)
        if sortNum:
            urlList.append("snum=" + sortNum)
        if sortType:
            urlList.append("sort=" + sortType)
        newUrl = "&".join(urlList)

        handleUrl = "comments?" + newUrl
        return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                      locals())

    if request.GET.get("iscom"):
        cidData = request.GET.get("cid")
        commentData = currency.models.CommentsModel.objects.get(cid=cidData)
        try:
            if commentData.is_recommend == True:
                currency.models.CommentsModel.objects.filter(cid=cidData).update(is_recommend=False)
            else:
                currency.models.CommentsModel.objects.filter(cid=cidData).update(is_recommend=True)
        except:
            pass
        return redirect(request.META['HTTP_REFERER'])

    if request.GET.get("watched"):
        cidData = request.GET.get("cid")
        commentData = currency.models.CommentsModel.objects.get(cid=cidData)
        try:
            if commentData.watched == True:
                currency.models.CommentsModel.objects.filter(cid=cidData).update(watched=False)
            else:
                currency.models.CommentsModel.objects.filter(cid=cidData).update(watched=True)
        except:
            pass
            return redirect(request.META['HTTP_REFERER'])

    # 此处从数据库中提取数据
    commentAll = currency.models.CommentsModel.objects.filter(pid=None).order_by("-cid")

    # 进行数据排序，根据前端传递过来的参数，可能有ID，name，type，sort以及date等五种排序，其中ID排序为默认排序
    # 接受数据，其中sortNum是顺序方向，1表示从大到小，其他表示从小到大
    sortType = request.GET.get("sort")
    sortNum = request.GET.get("snum", "1")

    # 这里是设置默认排序为ID，并且提取出defaultString便于前端使用，保持前后url的一致性
    if sortType:
        defaultString = "sort=%s&snum=%s" % (sortType, sortNum)
    else:
        defaultString = ""
        sortType = "id"
    # 这里是进行排序
    if sortType == "username":
        if sortNum == "1":
            commentAll = commentAll.order_by("-username")
        else:
            commentAll = commentAll.order_by("username")
    elif sortType == "time":
        if sortNum == "1":
            commentAll = commentAll.order_by("-date_publish")
        else:
            commentAll = commentAll.order_by("date_publish")
    elif sortType == "title":
        if sortNum == "1":
            commentAll = commentAll.order_by("-article")
        else:
            commentAll = commentAll.order_by("article")
    else:
        commentAll = commentAll.order_by("-cid")

    # 用于数据的前端使用，由于前端想要用count这个参数，所以此处需要单独二次处理

    # 对页码进行处理，并进行分页
    # 页码只接受传递进来的数字类型，默认是1
    try:
        pageNum = int(request.GET.get("page", 1))
    except Exception as e:
        errorLogger(e)
        pageNum = 1
    # 进行分页，此处为分页器分页，默认每页5条数据
    paginator = Paginator(commentAll, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    commentList = paginator.page(pageNum)



    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "commentView.html"), locals())


@csrf_exempt
def adminPhotoAdd(request):
    '''
    此功能添加照片
    :param request:
    :return:
    '''
    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("photo")
    nextNavBar = navbar["photo"]["nextDir"]
    pageTitle = "上传图片"
    categoryData = currency.models.CategoryModel.objects.filter(type=3)
    tagsData = currency.models.TagsModel.objects.filter(type=3)

    # 判断查看文章的上一层路径，此处不可以用refer_http，因为中间经历过跳转
    # 主要是判断来源是分类归类中/标签归类中来源，handleUrl是handle页面跳转URL
    iidData = request.GET.get("iid")
    tempUrlData = str(request.get_full_path()).replace("iid=%s" % (iidData), "").replace("?&", "?")
    if "cid" in tempUrlData:
        handleUrl = tempUrlData.replace("uploadPhoto", "addCategory")
    elif "tid" in tempUrlData:
        handleUrl = tempUrlData.replace("uploadPhoto", "addTag")
    else:
        handleUrl = "viewPhoto?sort=date&snum=1"

    if iidData:
        # 修改，修改时不支持图像的上传
        try:
            photoInDb = album.models.ImagesModel.objects.get(iid=iidData)
            fileInDb = photoInDb.picture
            picUrl = "/files/" + fileInDb.file_add
            pageTitle = "图片修改"
        except Exception as e:
            errorLogger(e)
            saveToDB = ("danger", "该数据已不再数据库中，查询失败！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                          locals())

    if request.method == "POST":
        filedata = request.FILES.getlist("upfile")
        getCategory = request.POST.get("category")
        getTag = request.POST.get("tag")
        isRecommend = request.POST.get("recommend")
        fileNameDataIID = request.POST.get("name")

        if getTag:
            if "," in getTag:
                getTag = getTag.split(",")
            else:
                getTag = [getTag, ]

        timeDataYear, timeDataMonth, timeDataDay, timeDataHour, timeDataMinute, timeDataSecond = currency.views.newTime()

        if iidData:
            # 修改，修改时不支持图像的上传
            try:
                saveToDbCategoryData = currency.models.CategoryModel.objects.get(cid=getCategory, type=3)

                photoData = album.models.ImagesModel.objects.filter(iid=iidData).update(
                    is_recommend=isRecommend,
                    album=saveToDbCategoryData,
                    name=fileNameDataIID,
                )
                photoData = album.models.ImagesModel.objects.get(iid=iidData)
                photoData.tag.clear()
                if getTag:
                    for eveTag in getTag:
                        if eveTag:
                            # 判断tags是否存在，不出异常表示存在，出现异常表示不存在，则新建
                            try:
                                tag_obj = currency.models.TagsModel.objects.get(name=eveTag, type="3")
                            except Exception as e:
                                tag_obj = currency.models.TagsModel.objects.create(name=eveTag, type="3",
                                                                                   unique="%s-%s" % (
                                                                                   str(eveTag), str("3")))
                            photoData.tag.add(tag_obj)
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "更新失败，请检查错误日志后者稍后重试。")
            saveToDB = ("success", "更新成功！为您跳转到列表页面！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                          locals())

        else:
            # 新建，需要上传图像
            try:
                for eveFile in filedata:
                    try:
                        fileNameList = str(eveFile.name).split(".")
                        fileName = ".".join(fileNameList[0:(int(len(fileNameList)) - 1)])
                        fileType = fileNameList[-1]
                        md5NameDate = currency.views.md5(
                            (str(int(time.time())) + fileName).encode("utf-8")) + "." + fileType
                        savePath = "photo/%s-%s-%s/%s" % (
                        str(timeDataYear), str(timeDataMonth), str(timeDataDay), md5NameDate)

                        path = default_storage.save(savePath, ContentFile(eveFile.read()))
                        tmpFile = os.path.join(BlogSystem.settings.MEDIA_ROOT, path)
                        fileMd5 = currency.views.getFileMd5(tmpFile)

                        '''
                        fid = models.AutoField(primary_key=True)
                        md5 = models.CharField(max_length=100,unique=True, verbose_name="md5")
                        name = models.CharField(max_length=100,verbose_name="名称")
                        file_add = models.CharField(max_length=100,verbose_name="附件地址")
                        type = models.CharField(max_length=100,verbose_name="附件类型")
                        size = models.IntegerField(default=0, verbose_name="大小")
                        date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
                        category = models.CharField(max_length=100, verbose_name="分类")
                        '''

                        # 实现图片的上传，将图片放入数据库
                        fileData = currency.models.FileModel.objects.create(
                            md5=fileMd5,
                            name=fileName,
                            file_add=path,
                            type=fileType,
                            size=eveFile.size,
                            category="3"
                        )

                        # 数据存入ImageModel数据库
                        '''
                        iid = models.AutoField(primary_key=True)
                        picture = models.ForeignKey(FileModel,verbose_name="图片")
                        is_recommend = models.BooleanField(default=True, verbose_name="是否显示")
                        index = models.IntegerField(default=999, verbose_name="排序")
                        tag = models.ManyToManyField(TagsModel, verbose_name="标签")
                        album = models.ForeignKey(CategoryModel, blank=True, null=True, verbose_name="相册")
                        '''

                        saveToDbCategoryData = currency.models.CategoryModel.objects.get(cid=getCategory, type=3)

                        photoData = album.models.ImagesModel.objects.create(
                            picture=fileData,
                            is_recommend=isRecommend,
                            album=saveToDbCategoryData,
                            name=fileName,
                        )

                        if getTag:
                            for eveTag in getTag:
                                if eveTag:
                                    # 判断tags是否存在，不出异常表示存在，出现异常表示不存在，则新建
                                    try:
                                        tag_obj = currency.models.TagsModel.objects.get(name=eveTag, type="3")
                                    except Exception as e:
                                        tag_obj = currency.models.TagsModel.objects.create(name=eveTag, type="3",
                                                                                           unique="%s-%s" % (
                                                                                           str(eveTag), str("3")))
                                    photoData.tag.add(tag_obj)
                    except Exception as e:
                        errorLogger(e)
                        saveToDB = ("warning", "添加失败，请检查错误日志后者稍后重试。")
            except Exception as e:
                # 整体出错！非常严重！
                errorLogger(e)
                saveToDB = ("warning", "添加失败，请检查错误日志后者稍后重试。")
            saveToDB = ("success", "添加成功！为您跳转到列表页面！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                          locals())

    pageTitle = "上传图片"
    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "photoAdd.html"), locals())


def adminPhotoView(request):
    '''
    此功能查看照片列表
    :param request:
    :return:
    '''
    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("photo")
    nextNavBar = navbar["photo"]["nextDir"]

    pageTitle = "图片列表"

    # 获取整体url
    pageUrl = request.get_raw_uri()

    # 此处进行删除操作
    if request.GET.get("dele"):
        # 如果请求的参数仲有dele和aid，则进行删除操作
        deleIidData = request.GET.get("iid")
        if deleIidData:
            try:
                deleResult = album.models.ImagesModel.objects.filter(iid=int(deleIidData)).delete()
                if deleResult[0] == 0:
                    saveToDB = ("danger", "删除失败！未发现该条数据！")
                else:
                    saveToDB = ("success", "删除成功！为您刷新列表页面！")
            except Exception as e:
                errorLogger(e)
                saveToDB = ("danger", "删除失败，请检查数据是否存在！")
        else:
            saveToDB = ("danger", "删除失败，请检查参数是否正确！")

        # 删除之后的数据跳转操作
        urlList = []
        pageNum = request.GET.get("page")
        sortNum = request.GET.get("snum")
        sortType = request.GET.get("sort")
        if pageNum:
            urlList.append("page=" + pageNum)
        if sortNum:
            urlList.append("snum=" + sortNum)
        if sortType:
            urlList.append("sort=" + sortType)
        newUrl = "&".join(urlList)

        handleUrl = "viewPhoto?" + newUrl
        return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                      locals())

    # 此处从数据库中提取数据
    photoAll = album.models.ImagesModel.objects.all().order_by("-iid")

    # 进行数据排序，根据前端传递过来的参数，可能有ID，name，type，sort以及date等五种排序，其中ID排序为默认排序
    # 接受数据，其中sortNum是顺序方向，1表示从大到小，其他表示从小到大
    sortType = request.GET.get("sort")
    sortNum = request.GET.get("snum", "1")

    # 这里是设置默认排序为ID，并且提取出defaultString便于前端使用，保持前后url的一致性
    if sortType:
        defaultString = "sort=%s&snum=%s" % (sortType, sortNum)
    else:
        defaultString = ""
        sortType = "id"
    # 这里是进行排序
    if sortType == "title":
        if sortNum == "1":
            photoAll = photoAll.order_by("-name")
        else:
            photoAll = photoAll.order_by("name")
    elif sortType == "date_publish" or sortType == "date":
        if sortNum == "1":
            photoAll = photoAll.order_by("-iid")
        else:
            photoAll = photoAll.order_by("iid")
    elif sortType == "category":
        if sortNum == "1":
            photoAll = photoAll.order_by("-album")
        else:
            photoAll = photoAll.order_by("album")
    else:
        photoAll = photoAll.order_by("-iid")

    # 对页码进行处理，并进行分页
    # 页码只接受传递进来的数字类型，默认是1
    try:
        pageNum = int(request.GET.get("page", 1))
    except Exception as e:
        errorLogger(e)
        pageNum = 1
    # 进行分页，此处为分页器分页，默认每页5条数据
    paginator = Paginator(photoAll, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    photoList = paginator.page(pageNum)

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "photoView.html"), locals())


@csrf_exempt
def adminFileAdd(request):
    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("file")
    nextNavBar = navbar["file"]["nextDir"]

    pageTitle = "上传文件"

    if request.method == "POST":
        try:
            for eveFile in request.FILES.getlist("file_data"):
                timeDataYear, timeDataMonth, timeDataDay, timeDataHour, timeDataMinute, timeDataSecond = currency.views.newTime()
                try:
                    fileNameList = str(eveFile.name).split(".")
                    fileName = ".".join(fileNameList[0:(int(len(fileNameList)) - 1)])
                    fileType = fileNameList[-1]
                except Exception as e:
                    errorLogger(e)
                    fileName = eveFile.name
                    fileType = ""
                md5NameDate = currency.views.md5((str(int(time.time())) + fileName).encode("utf-8")) + "." + fileType
                savePath = "files/%s-%s-%s/%s" % (str(timeDataYear), str(timeDataMonth), str(timeDataDay), md5NameDate)

                path = default_storage.save(savePath, ContentFile(eveFile.read()))
                tmpFile = os.path.join(BlogSystem.settings.MEDIA_ROOT, path)
                fileMd5 = currency.views.getFileMd5(tmpFile)

                '''
                fid = models.AutoField(primary_key=True)
                md5 = models.CharField(max_length=100,unique=True, verbose_name="md5")
                name = models.CharField(max_length=100,verbose_name="名称")
                file_add = models.CharField(max_length=100,verbose_name="附件地址")
                type = models.CharField(max_length=100,verbose_name="附件类型")
                size = models.IntegerField(default=0, verbose_name="大小")
                date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
                category = models.CharField(max_length=100, verbose_name="分类")
                '''

                # 实现图片的上传，将图片放入数据库
                fileData = currency.models.FileModel.objects.create(
                    md5=fileMd5,
                    name=fileName,
                    file_add=path,
                    type=fileType,
                    size=eveFile.size,
                    category="2"  # 本页上传2，相册上传3，文章上传0，项目上传1
                )
            return HttpResponse("1")
        except Exception as e:
            errorLogger(e)
            return HttpResponse("0")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "fileAdd.html"), locals())


def adminFileView(request):
    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("file")
    nextNavBar = navbar["file"]["nextDir"]

    pageTitle = "文件列表"

    # 获取整体url
    pageUrl = request.get_raw_uri()

    # 此处进行删除操作
    # if request.GET.get("dele"):
    #     # 如果请求的参数仲有dele和aid，则进行删除操作
    #     deleIidData = request.GET.get("fid")
    #     if deleIidData:
    #         try:
    #             deleResult = currency.models.FileModel.objects.filter(fid=int(deleIidData)).delete()
    #             if deleResult[0] == 0:
    #                 saveToDB = ("danger", "删除失败！未发现该条数据！")
    #             else:
    #                 saveToDB = ("success", "删除成功！为您刷新列表页面！")
    #         except Exception as e:
    #             errorLogger(e)
    #             saveToDB = ("danger", "删除失败，请检查数据是否存在！")
    #     else:
    #         saveToDB = ("danger", "删除失败，请检查参数是否正确！")
    #
    #     # 删除之后的数据跳转操作
    #     urlList = []
    #     pageNum = request.GET.get("page")
    #     sortNum = request.GET.get("snum")
    #     sortType = request.GET.get("sort")
    #     if pageNum:
    #         urlList.append("page=" + pageNum)
    #     if sortNum:
    #         urlList.append("snum=" + sortNum)
    #     if sortType:
    #         urlList.append("sort=" + sortType)
    #     newUrl = "&".join(urlList)
    #
    #     handleUrl = "viewFile?" + newUrl
    #     return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),locals())

    # 此处从数据库中提取数据
    fileAll = currency.models.FileModel.objects.all().order_by("-fid")

    # 进行数据排序，根据前端传递过来的参数，可能有ID，name，type，sort以及date等五种排序，其中ID排序为默认排序
    # 接受数据，其中sortNum是顺序方向，1表示从大到小，其他表示从小到大
    sortType = request.GET.get("sort")
    sortNum = request.GET.get("snum", "1")

    # 这里是设置默认排序为ID，并且提取出defaultString便于前端使用，保持前后url的一致性
    if sortType:
        defaultString = "sort=%s&snum=%s" % (sortType, sortNum)
    else:
        defaultString = ""
        sortType = "id"
    # 这里是进行排序
    if sortType == "title":
        if sortNum == "1":
            fileAll = fileAll.order_by("-name")
        else:
            fileAll = fileAll.order_by("name")
    elif sortType == "date_publish" or sortType == "date":
        if sortNum == "1":
            fileAll = fileAll.order_by("-fid")
        else:
            fileAll = fileAll.order_by("fid")
    elif sortType == "category":
        if sortNum == "1":
            fileAll = fileAll.order_by("-category")
        else:
            fileAll = fileAll.order_by("category")
    elif sortType == "type":
        if sortNum == "1":
            fileAll = fileAll.order_by("-type")
        else:
            fileAll = fileAll.order_by("type")
    else:
        fileAll = fileAll.order_by("fid")

    # 对页码进行处理，并进行分页
    # 页码只接受传递进来的数字类型，默认是1
    try:
        pageNum = int(request.GET.get("page", 1))
    except Exception as e:
        errorLogger(e)
        pageNum = 1
    # 进行分页，此处为分页器分页，默认每页5条数据
    paginator = Paginator(fileAll, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    fileList = paginator.page(pageNum)

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "fileView.html"), locals())


@csrf_exempt
def adminUserAdd(request):
    '''
    添加用户页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基础信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("user")
    nextNavBar = navbar["user"]["nextDir"]
    pageTitle = "用户列表"

    handleUrl = "viewUser?sort=date&snum=1"
    photoFile = []
    for evePhoto in range(1, 41):
        photoFile.append((evePhoto, "/files/userFace/%d.jpg" % (evePhoto)))

    # 如果有uid的参数，代表这是查看功能
    uidData = request.GET.get("uid")
    if uidData:
        try:
            userDataView = usercenter.models.UserModel.objects.get(uid=int(uidData))
            userNameView = userDataView.username
            userSexView = userDataView.sex
            userEmailView = userDataView.email
            userPhoneView = userDataView.phone
            userQQView = userDataView.qq
            userTypeView = userDataView.type
            userPasswordView = userDataView.password
            userStateView = userDataView.state
            userPhotoView = userDataView.photo
            pageTitle = "修改用户"
        except Exception as e:
            errorLogger(e)
            saveToDB = ("danger", "该数据已不再数据库中，查询失败！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                          locals())

    # 如果请求模式是post，则表示提交了数据
    if request.method == "POST":

        # 获取提交的数据
        userName = request.POST.get("name")
        userSex = request.POST.get("sex")
        userEmail = request.POST.get("email")
        userPhone = request.POST.get("phone")
        userQQ = request.POST.get("qq")
        userType = request.POST.get("type")
        userPassword = request.POST.get("password")
        userState = request.POST.get("state")
        userPhoto = request.POST.get("photo")

        # 如果非法提交了userName和userPassword，则发出警告
        if not userName or not userPassword:
            saveToDB = ("warning", "用户名称和密码是必选内容，必须填写！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "userAdd.html"),
                          locals())

        # 如果有uidData，则表示这个是查看并且修改
        if uidData:
            try:
                '''
                    uid = models.AutoField(primary_key=True)
                    username = models.CharField(max_length=30,unique=True, verbose_name="用户名")
                    sex = models.CharField(max_length=10, null=True,verbose_name="性别")
                    email = models.CharField(max_length=30, verbose_name="邮箱")
                    photo = models.CharField(default="/static/currency/userohoto/default/user.png",max_length=100,null=True,verbose_name="头像")
                    wechat = models.CharField(max_length=30,null=True, verbose_name="微信")
                    qq = models.CharField(max_length=30, null=True, verbose_name="QQ")
                    phone = models.CharField(max_length=30, null=True, verbose_name="电话")
                    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
                    password = models.CharField(max_length=30, verbose_name="密码")
                    type = models.CharField(max_length=30, verbose_name="类型")
                    state = models.BooleanField(default=True, verbose_name="状态")
                '''
                userDBModel = usercenter.models.UserModel.objects.filter(uid=int(uidData)).update(
                    username=userName,
                    sex=userSex,
                    qq=userQQ,
                    email=userEmail,
                    password=userPassword,
                    state=userState,
                    type=userType,
                    phone=userPhone,
                    photo=userPhoto,
                )
                saveToDB = ("success", "修改成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "修改失败，请检查是否之前已经添加过类似的内容。")

        else:
            # 否则是新建数据
            try:
                '''
                    cid = models.AutoField(primary_key=True)
                    name = models.CharField(max_length=30, verbose_name="名称")
                    index = models.IntegerField(default=999, verbose_name="排序")
                    date = models.DateTimeField(auto_now_add=True, verbose_name="时间")
                    remark = models.CharField(max_length=150, verbose_name="备注说明")
                    type = models.CharField(max_length=30, verbose_name="类型")
                    unique = models.CharField(max_length=150, unique=True, verbose_name="唯一性判断")
                '''
                userDBModel = usercenter.models.UserModel.objects.create(
                    username=userName,
                    sex=userSex,
                    qq=userQQ,
                    email=userEmail,
                    phone=userPhone,
                    password=userPassword,
                    state=userState,
                    type=userType,
                    photo=userPhoto,
                )
                saveToDB = ("success", "添加成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "添加失败，请检查是否之前已经添加过类似的内容。")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "userAdd.html"), locals())


def adminUserView(request):
    '''
    用户查看列表
    :param request:
    :return:
    '''
    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基础信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("user")
    nextNavBar = navbar["user"]["nextDir"]
    pageTitle = "用户列表"

    # 获取整体url
    pageUrl = request.get_raw_uri()

    # 此处进行删除操作
    if request.GET.get("dele"):
        # 如果请求的参数仲有dele和cid，则进行删除操作
        deleUidData = request.GET.get("uid")
        if deleUidData:
            try:
                deleResult = usercenter.models.UserModel.objects.filter(uid=int(deleUidData)).delete()
                if deleResult[0] == 0:
                    saveToDB = ("danger", "删除失败！未发现该条数据！")
                else:
                    saveToDB = ("success", "删除成功！为您刷新列表页面！")
            except Exception as e:
                errorLogger(e)
                saveToDB = ("danger", "删除失败，请检查数据是否存在！")
        else:
            saveToDB = ("danger", "删除失败，请检查参数是否正确！")

        # 删除之后的数据跳转操作
        urlList = []
        pageNum = request.GET.get("page")
        sortNum = request.GET.get("snum")
        sortType = request.GET.get("sort")
        if pageNum:
            urlList.append("page=" + pageNum)
        if sortNum:
            urlList.append("snum=" + sortNum)
        if sortType:
            urlList.append("sort=" + sortType)
        newUrl = "&".join(urlList)

        handleUrl = "viewUser?" + newUrl
        return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                      locals())

    # 此处从数据库中提取数据
    userAll = usercenter.models.UserModel.objects.all()

    # 进行数据排序，根据前端传递过来的参数，可能有ID，name，type，sort以及date等五种排序，其中ID排序为默认排序
    # 接受数据，其中sortNum是顺序方向，1表示从大到小，其他表示从小到大
    sortType = request.GET.get("sort")
    sortNum = request.GET.get("snum", "1")

    # 这里是设置默认排序为ID，并且提取出defaultString便于前端使用，保持前后url的一致性
    if sortType:
        defaultString = "sort=%s&snum=%s" % (sortType, sortNum)
    else:
        defaultString = ""
        sortType = "id"
    # 这里是进行排序
    if sortType == "name":
        if sortNum == "1":
            userAll = userAll.order_by("-name")
        else:
            userAll = userAll.order_by("name")
    elif sortType == "date":
        if sortNum == "1":
            userAll = userAll.order_by("-date")
        else:
            userAll = userAll.order_by("date")
    else:
        userAll = userAll.order_by("uid")

    # 对页码进行处理，并进行分页
    # 页码只接受传递进来的数字类型，默认是1
    try:
        pageNum = int(request.GET.get("page", 1))
    except Exception as e:
        errorLogger(e)
        pageNum = 1
    # 进行分页，此处为分页器分页，默认每页5条数据
    paginator = Paginator(userAll, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    userList = paginator.page(pageNum)

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "userView.html"), locals())


@csrf_exempt
def adminResumeAdd(request):
    '''
    添加简历信息页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("resume")
    nextNavBar = navbar["resume"]["nextDir"]
    pageTitle = "添加简历信息"

    handleUrl = "viewResume"

    # 如果有cid的参数，代表这是查看功能
    ridData = request.GET.get("rid")
    if ridData:
        try:
            resumeDataView = resume.models.ResumeModel.objects.get(rid=int(ridData))
            pageTitle = "修改分类"

        except Exception as e:
            errorLogger(e)
            saveToDB = ("danger", "该数据已不再数据库中，查询失败！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                          locals())

    # 如果请求模式是post，则表示提交了数据
    if request.method == "POST":

        # 获取提交的数据
        resumeKey = request.POST.get("key")
        resumeValue = request.POST.get("value")

        # 如果有cidData，则表示这个是查看并且修改
        if ridData:
            try:
                # 更新数据
                resumeDBModel = resume.models.ResumeModel.objects.filter(rid=int(ridData)).update(
                    keyData = resumeKey,
                    valueData = resumeValue,
                )
                saveToDB = ("success", "修改成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "修改失败，请检查是否之前已经添加过类似的内容。")

        else:
            # 否则是新建数据
            try:
                # 新建数据
                resumeDBModel = resume.models.ResumeModel.objects.create(
                    keyData=resumeKey,
                    valueData=resumeValue,
                )
                saveToDB = ("success", "添加成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                errorLogger(e)
                saveToDB = ("warning", "添加失败，请检查是否之前已经添加过类似的内容。")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "resumeAdd.html"), locals())


def adminResume(request):
    '''
        简历查看页面
        :param request:
        :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("resume")
    nextNavBar = navbar["resume"]["nextDir"]
    pageTitle = "简历页面"

    # 获取整体url
    pageUrl = request.get_raw_uri()

    # 此处进行删除操作
    if request.GET.get("dele"):
        # 如果请求的参数仲有dele和cid，则进行删除操作
        deleRidData = request.GET.get("rid")
        if deleRidData:
            try:
                deleResult = resume.models.ResumeModel.objects.filter(rid=int(deleRidData)).delete()
                if deleResult[0] == 0:
                    saveToDB = ("danger", "删除失败！未发现该条数据！")
                else:
                    saveToDB = ("success", "删除成功！为您刷新列表页面！")
            except Exception as e:
                errorLogger(e)
                saveToDB = ("danger", "删除失败，请检查数据是否存在！")
        else:
            saveToDB = ("danger", "删除失败，请检查参数是否正确！")

        # 删除之后的数据跳转操作
        urlList = []
        pageNum = request.GET.get("page")
        sortNum = request.GET.get("snum")
        sortType = request.GET.get("sort")
        if pageNum:
            urlList.append("page=" + pageNum)
        if sortNum:
            urlList.append("snum=" + sortNum)
        if sortType:
            urlList.append("sort=" + sortType)
        newUrl = "&".join(urlList)

        handleUrl = "viewResume?" + newUrl
        return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                      locals())

    # 此处从数据库中提取数据
    rusumenAll = resume.models.ResumeModel.objects.all().order_by("-rid")

    # 对页码进行处理，并进行分页
    # 页码只接受传递进来的数字类型，默认是1
    try:
        pageNum = int(request.GET.get("page", 1))
    except Exception as e:
        errorLogger(e)
        pageNum = 1
    # 进行分页，此处为分页器分页，默认每页5条数据
    paginator = Paginator(rusumenAll, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    resumeList = paginator.page(pageNum)

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "resumeView.html"), locals())



@csrf_exempt
def adminVideoAdd(request):
    '''
    添加视频信息页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("video")
    nextNavBar = navbar["video"]["nextDir"]
    pageTitle = "添加视频"

    handleUrl = "viewVideo?sort=date&snum=1"

    # 如果有cid的参数，代表这是查看功能
    vidData = request.GET.get("vid")
    if vidData:
        try:
            videoDataView = video.models.VideoModel.objects.get(vid=int(vidData))
            videoNameView = videoDataView.name
            videoNumberList = videoDataView.numberList
            if "&number&" in videoNumberList:
                videoNumberList = videoNumberList.split("&number&")
            else:
                videoNumberList = [videoNumberList]
            videoNumberListView = ",".join(videoNumberList)
            pageTitle = "修改视频信息"

        except Exception as e:
            errorLogger(e)
            saveToDB = ("danger", "该数据已不再数据库中，查询失败！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),locals())

    # 如果请求模式是post，则表示提交了数据
    if request.method == "POST":

        # 获取提交的数据
        videoName = request.POST.get("name")
        videoNumber = request.POST.get("number")
        if "," in videoNumber:
            videoNumber = videoNumber.split(",")
        else:
            videoNumber = [videoNumber,]

        tempNumber = []
        for eveNumber in videoNumber:
            if eveNumber not in tempNumber:
                tempNumber.append(eveNumber)
        videoNumber = tempNumber

        # 如果非法提交了categoryName和categoryType，则发出警告
        if not videoName :
            saveToDB = ("warning", "视频分类名是必选内容，必须填写！")
            return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "videoAdd.html"),locals())

        # 如果有cidData，则表示这个是查看并且修改
        if vidData:
            try:
                '''
                    vid = models.AutoField(primary_key=True)
                    name = models.CharField(max_length=255)
                    titleList = models.TextField()
                    numberList = models.TextField()
                    urlList = models.TextField()
                '''
                # 更新数据
                urlList = []
                titleList = []
                for eveAVData in videoNumber:
                    try:
                        tempUrl,tempTitle = getBilibiliData(eveAVData)
                        urlList.append(tempUrl)
                        titleList.append(tempTitle)
                    except Exception as e:
                        print(e)
                        errorLogger(e)

                videoDBModel = video.models.VideoModel.objects.filter(vid=int(vidData)).update(
                    name = videoName,
                    numberList = "&number&".join(videoNumber),
                    titleList = "&title&".join(titleList),
                    urlList = "&url&".join(urlList),

                )
                saveToDB = ("success", "修改成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                print(e)
                errorLogger(e)
                saveToDB = ("warning", "修改失败，请检查是否之前已经添加过类似的内容。")

        else:
            # 否则是新建数据
            try:
                '''
                    vid = models.AutoField(primary_key=True)
                    name = models.CharField(max_length=255)
                    titleList = models.TextField()
                    numberList = models.TextField()
                    
                '''
                # 更新数据
                urlList = []
                titleList = []
                for eveAVData in videoNumber:
                    try:
                        tempUrl, tempTitle = getBilibiliData(eveAVData)
                        urlList.append(tempUrl)
                        titleList.append(tempTitle)
                    except Exception as e:
                        errorLogger(e)

                videoDBModel = video.models.VideoModel.objects.create(
                    name=videoName,
                    numberList=videoNumber,
                    titleList="&title&".join(titleList),
                    urlList="&url&".join(urlList),

                )
                saveToDB = ("success", "添加成功！为您跳转到列表页面！")
                return render(request,
                              "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                              locals())
            except Exception as e:
                print(2,e)
                errorLogger(e)
                saveToDB = ("warning", "添加失败，请检查是否之前已经添加过类似的内容。")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "videoAdd.html"), locals())


def adminVideoView(request):
    '''
    视频查看页面
    :param request:
    :return:
    '''

    # 判断用户是否登陆，同时判断用户登录的是否是管理员账号
    try:
        isLogin = isLoginTrue(request)
        if isLogin == 0 or isLogin == -1:
            redirectTitle = "超出权限，请登录管理员账号后再执行操作"
            redirectUrl = "/login"
            return render(request, "currency/loginAndRegister/handle.html", locals())
        else:
            if isLogin[1] == "1":
                loginUid = isLogin[2]
            else:
                redirectTitle = "管理员功能，普通用户无权限操作"
                redirectUrl = "/login"
                return render(request, "currency/loginAndRegister/handle.html", locals())
    except Exception as e:
        redirectTitle = "超出权限，请登录管理员账号后再执行操作"
        redirectUrl = "/login"
        return render(request, "currency/loginAndRegister/handle.html", locals())
    # 判断是否管理登陆完成，如果是，则执行以下代码，否则已经在上述代码中跳转到指定页面。

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("video")
    nextNavBar = navbar["video"]["nextDir"]
    pageTitle = "视频列表"

    # 获取整体url
    pageUrl = request.get_raw_uri()

    # 此处进行删除操作
    if request.GET.get("dele"):
        # 如果请求的参数仲有dele和cid，则进行删除操作
        deleVidData = request.GET.get("vid")
        if deleVidData:
            try:
                deleResult = video.models.VideoModel.objects.filter(vid=int(deleVidData)).delete()
                if deleResult[0] == 0:
                    saveToDB = ("danger", "删除失败！未发现该条数据！")
                else:
                    saveToDB = ("success", "删除成功！为您刷新列表页面！")
            except Exception as e:
                errorLogger(e)
                saveToDB = ("danger", "删除失败，请检查数据是否存在！")
        else:
            saveToDB = ("danger", "删除失败，请检查参数是否正确！")

        # 删除之后的数据跳转操作
        urlList = []
        pageNum = request.GET.get("page")
        sortNum = request.GET.get("snum")
        sortType = request.GET.get("sort")
        if pageNum:
            urlList.append("page=" + pageNum)
        if sortNum:
            urlList.append("snum=" + sortNum)
        if sortType:
            urlList.append("sort=" + sortType)
        newUrl = "&".join(urlList)

        handleUrl = "viewVideo?" + newUrl
        return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "handleResult.html"),
                      locals())

    # 此处从数据库中提取数据
    videoAll = video.models.VideoModel.objects.all().order_by("-vid")

    # 对页码进行处理，并进行分页
    # 页码只接受传递进来的数字类型，默认是1
    try:
        pageNum = int(request.GET.get("page", 1))
    except Exception as e:
        errorLogger(e)
        pageNum = 1
    # 进行分页，此处为分页器分页，默认每页5条数据
    paginator = Paginator(videoAll, 10)
    # 对传递过来的页面进行判断，页码最小为1，最大为分页器所得总页数
    if pageNum < 0:
        pageNum = 1
    if pageNum > paginator.num_pages:
        pageNum = paginator.num_pages
    # 分页器获得当前页面的数据内容
    videoList = paginator.page(pageNum)

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "videoView.html"), locals())



def adminTimeLine(request):
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("show")
    nextNavBar = navbar["show"]["nextDir"]

    pageTitle = "记录时光"
    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "index.html"), locals())


@csrf_exempt
def adminWebSetting(request):
    '''
    实现网站整体功能设置
    :param request:
    :return:
    '''

    # 页面标题
    pageTitle = "系统信息设置"

    # 如果是POST请求，则说明相关数据可能需要修改，
    if request.method == "POST":
        # 从前端获取数据
        webHost = str(request.POST.get("web", "暂无")).replace("webHost", "WEBHOST")
        webName = request.POST.get("name", "暂无").replace("webName", "WEBNAME")
        webKeyword = request.POST.get("keyword", "暂无").replace("webKeyword", "WEBKEYWORD")
        webDescription = request.POST.get("desc", "暂无").replace("webDescription", "WEBDESCRIPTION")

        # 通过文件读取方法获得全部数据
        with open("BlogSystem/base.conf") as f:
            readData = f.readlines()

        # 通过文件写入方法更新数据
        with open("BlogSystem/base.conf", "w") as f:
            for eveLine in readData:
                if "webHost:" in eveLine:
                    f.write("%swebHost:%s\n" % (eveLine.split("webHost:")[0], webHost))
                elif "webName:" in eveLine:
                    f.write("%swebName:%s\n" % (eveLine.split("webName:")[0], webName))
                elif "webKeyword:" in eveLine:
                    f.write("%swebKeyword:%s\n" % (eveLine.split("webKeyword:")[0], webKeyword))
                elif "webDescription:" in eveLine:
                    f.write("%swebDescription:%s\n" % (eveLine.split("webDescription:")[0], webDescription))
                else:
                    f.write(eveLine)
        saveToDB = ("success", "<" + pageTitle + ">修改成功！")

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("setting")
    nextNavBar = navbar["setting"]["nextDir"]

    # 前台所需显示的数据
    webHostView = information.getValue("webHost")
    webNameView = information.getValue("webName")
    webKeywordView = information.getValue("webKeyword")
    webDescriptionView = information.getValue("webDescription")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "settingWeb.html"), locals())


@csrf_exempt
def adminMysqlSetting(request):
    '''
    数显数据库设置功能
    :param request:
    :return:
    '''

    # 页面标题
    pageTitle = "数据库设置"

    # 如果是POST请求，则说明相关数据可能需要修改，
    if request.method == "POST":
        # 从前端获取数据
        mysqlHost = str(request.POST.get("host", "暂无")).replace("mysqlHost", "MYSQLHOST")
        mysqlPort = request.POST.get("port", "暂无").replace("mysqlPort", "MYSQLPORT")
        mysqlName = request.POST.get("name", "暂无").replace("mysqlName", "MYSQLNAME")
        mysqlUser = request.POST.get("user", "暂无").replace("mysqlUser", "MYSQLUSER")
        mysqlPassword = request.POST.get("password", "暂无").replace("mysqlPassword", "MYSQLPASSWORD")

        # 通过文件读取方法获得全部数据
        with open("BlogSystem/base.conf") as f:
            readData = f.readlines()

        # 通过文件写入方法更新数据
        with open("BlogSystem/base.conf", "w") as f:
            for eveLine in readData:
                if "mysqlHost:" in eveLine:
                    f.write("%smysqlHost:%s\n" % (eveLine.split("mysqlHost:")[0], mysqlHost))
                elif "mysqlPort:" in eveLine:
                    f.write("%smysqlPort:%s\n" % (eveLine.split("mysqlPort:")[0], mysqlPort))
                elif "mysqlName:" in eveLine:
                    f.write("%smysqlName:%s\n" % (eveLine.split("mysqlName:")[0], mysqlName))
                elif "mysqlUser:" in eveLine:
                    f.write("%smysqlUser:%s\n" % (eveLine.split("mysqlUser:")[0], mysqlUser))
                elif "mysqlPassword:" in eveLine:
                    f.write("%smysqlPassword:%s\n" % (eveLine.split("mysqlPassword:")[0], mysqlPassword))
                else:
                    f.write(eveLine)
        saveToDB = ("success", "<" + pageTitle + ">修改成功！")

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("setting")
    nextNavBar = navbar["setting"]["nextDir"]

    # 前台所需显示的数据
    mysqlHostView = information.getValue("mysqlHost")
    mysqlPortView = information.getValue("mysqlPort")
    mysqlNameView = information.getValue("mysqlName")
    mysqlUserView = information.getValue("mysqlUser")
    mysqlPasswordView = information.getValue("mysqlPassword")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "settingMysql.html"), locals())


@csrf_exempt
def adminEmailSetting(request):
    '''
    实现邮箱设置功能
    :param request:
    :return:
    '''

    # 页面标题
    pageTitle = "邮箱设置"

    # 如果是POST请求，则说明相关数据可能需要修改，
    if request.method == "POST":
        # 从前端获取数据
        emailUser = str(request.POST.get("user", "暂无")).replace("emailUser", "EMAILUSER")
        emailPassword = request.POST.get("password", "暂无").replace("emailPassword", "EMAILPASSWORD")
        emailPort = request.POST.get("port", "暂无").replace("emailPort", "EMAILPORT")
        emailSMTP = request.POST.get("smtp", "暂无").replace("emailSMTP", "EMAILSMTP")

        # 通过文件读取方法获得全部数据
        with open("BlogSystem/base.conf") as f:
            readData = f.readlines()

        # 通过文件写入方法更新数据
        with open("BlogSystem/base.conf", "w") as f:
            for eveLine in readData:
                if "emailUser:" in eveLine:
                    f.write("%semailUser:%s\n" % (eveLine.split("emailUser:")[0], emailUser))
                elif "emailPassword:" in eveLine:
                    f.write("%semailPassword:%s\n" % (eveLine.split("emailPassword:")[0], emailPassword))
                elif "emailPort:" in eveLine:
                    f.write("%semailPort:%s\n" % (eveLine.split("emailPort:")[0], emailPort))
                elif "emailSMTP:" in eveLine:
                    f.write("%semailSMTP:%s\n" % (eveLine.split("emailSMTP:")[0], emailSMTP))
                else:
                    f.write(eveLine)
        saveToDB = ("success", "<" + pageTitle + ">修改成功！")

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("setting")
    nextNavBar = navbar["setting"]["nextDir"]

    # 前台所需显示的数据
    emailUserView = information.getValue("emailUser")
    emailPasswordView = information.getValue("emailPassword")
    emailPortView = information.getValue("emailPort")
    emailSMTPView = information.getValue("emailSMTP")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "settingEmail.html"), locals())


@csrf_exempt
def adminOtherSetting(request):
    '''
    实现其他设置功能，例如访问的最大次数，模板信息等
    :param request:
    :return:
    '''

    # 页面标题
    pageTitle = "其他设置"

    # 如果是POST请求，则说明相关数据可能需要修改，
    if request.method == "POST":
        # 从前端获取数据
        templatesBlogName = str(request.POST.get("blog", "暂无")).replace("templatesBlogName", "TEMPLATESBLOGNAME")
        templatesAdminName = request.POST.get("admin", "暂无").replace("templatesAdminName", "TEMPLATESADMINNAME")
        templatesAlbumName = request.POST.get("album", "暂无").replace("templatesAlbumName", "TEMPLATESALBUMNAME")
        templatesVideoName = request.POST.get("video", "暂无").replace("templatesVideoName", "TEMPLATESVIDEONAME")
        templatesProjectName = request.POST.get("project", "暂无").replace("templatesProjectName", "TEMPLATESPROJECTNAME")
        templatesUserCenterName = request.POST.get("usercenter", "暂无").replace("templatesUserCenterName", "TEMPLATESUSERCENTERNAME")
        maxCounter = request.POST.get("max", "暂无").replace("maxCounter", "MAXCOUNTER")
        # 通过文件读取方法获得全部数据
        with open("BlogSystem/base.conf") as f:
            readData = f.readlines()

        # 通过文件写入方法更新数据
        with open("BlogSystem/base.conf", "w") as f:
            for eveLine in readData:
                if "templatesBlogName:" in eveLine:
                    f.write("%stemplatesBlogName:%s\n" % (eveLine.split("templatesBlogName:")[0], templatesBlogName))
                elif "templatesAdminName:" in eveLine:
                    f.write("%stemplatesAdminName:%s\n" % (eveLine.split("templatesAdminName:")[0], templatesAdminName))
                elif "templatesAlbumName:" in eveLine:
                    f.write("%stemplatesAlbumName:%s\n" % (eveLine.split("templatesAlbumName:")[0], templatesAlbumName))
                elif "templatesVideoName:" in eveLine:
                    f.write("%stemplatesVideoName:%s\n" % (eveLine.split("templatesVideoName:")[0], templatesVideoName))
                elif "templatesProjectName:" in eveLine:
                    f.write("%stemplatesProjectName:%s\n" % (eveLine.split("templatesProjectName:")[0], templatesProjectName))
                elif "templatesUserCenterName:" in eveLine:
                    f.write("%stemplatesUserCenterName:%s\n" % (eveLine.split("templatesUserCenterName:")[0], templatesUserCenterName))
                elif "maxCounter:" in eveLine:
                    f.write("%smaxCounter:%s\n" % (eveLine.split("maxCounter:")[0], maxCounter))
                else:
                    f.write(eveLine)
        saveToDB = ("success", "<" + pageTitle + ">修改成功！")

    # 网站基本信息
    information = Information()
    totalInfor = information.getAll()
    navbar = adminNavigation("setting")
    nextNavBar = navbar["setting"]["nextDir"]

    # 前台所需显示的数据
    templatesBlogNameView = information.getValue("templatesBlogName")
    templatesAdminNameView = information.getValue("templatesAdminName")
    templatesAlbumNameView = information.getValue("templatesAlbumName")
    templatesVideoNameView = information.getValue("templatesVideoName")
    templatesProjectNameView = information.getValue("templatesProjectName")
    templatesUserCenterNameView = information.getValue("templatesUserCenterName")
    maxCounterView = information.getValue("maxCounter")

    return render(request, "admin/%s/%s" % (information.getValue("templatesAdminName"), "settingOther.html"), locals())
