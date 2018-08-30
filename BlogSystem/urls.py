"""BlogSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from BlogSystem import settings
from django.views import static

import blog.views
import admin.views
import currency.views
import resume.views
import album.views
import video.views
import myproject.views
import usercenter.views
import apicenter.views

import tools.ueditor.views

urlpatterns = [

    # 后台页面
    url(r'^admin$', admin.views.adminArticleView),
    url(r'^admin/$', admin.views.adminArticleView),
    url(r'^admin/index$', admin.views.adminArticleView),
    url(r'^admin/addArticle', admin.views.adminArticleAdd),
    url(r'^admin/article$', admin.views.adminArticleView),
    url(r'^admin/viewArticle', admin.views.adminArticleView),
    url(r'^admin/addCategory$', admin.views.adminCategoryAdd),
    url(r'^admin/category$', admin.views.adminCategoryView),
    url(r'^admin/viewCategory$', admin.views.adminCategoryView),
    url(r'^admin/addTag$', admin.views.adminTagAdd),
    url(r'^admin/tag$', admin.views.adminTagView),
    url(r'^admin/viewTag$', admin.views.adminTagView),
    url(r'^admin/comments$', admin.views.adminComments),
    url(r'^admin/commentsView$', admin.views.adminCommentsAdd),
    url(r'^admin/uploadPhoto$', admin.views.adminPhotoAdd),
    url(r'^admin/photo$', admin.views.adminPhotoView),
    url(r'^admin/viewPhoto$', admin.views.adminPhotoView),
    url(r'^admin/addFile$', admin.views.adminFileAdd),
    url(r'^admin/file$', admin.views.adminFileView),
    url(r'^admin/viewFile', admin.views.adminFileView),
    url(r'^admin/viewUser$', admin.views.adminUserView),
    url(r'^admin/user$', admin.views.adminUserView),
    url(r'^admin/addUser$', admin.views.adminUserAdd),
    url(r'^admin/show$', admin.views.adminTimeLine),
    url(r'^admin/resume$', admin.views.adminResume),
    url(r'^admin/addResume$', admin.views.adminResumeAdd),
    url(r'^admin/viewResume$', admin.views.adminResume),
    url(r'^admin/video$', admin.views.adminVideoView),
    url(r'^admin/addVideo$', admin.views.adminVideoAdd),
    url(r'^admin/viewVideo$', admin.views.adminVideoView),
    url(r'^admin/timeline', admin.views.adminTimeLine),
    url(r'^admin/setting$', admin.views.adminWebSetting),
    url(r'^admin/webSetting', admin.views.adminWebSetting),
    url(r'^admin/mysqlSetting', admin.views.adminMysqlSetting),
    url(r'^admin/emailSetting', admin.views.adminEmailSetting),
    url(r'^admin/otherSetting', admin.views.adminOtherSetting),

    # 通用页面
    url(r'^sorry$', currency.views.maxCounterIndex),
    url(r'^wrong$', currency.views.wrongPageIndex),
    url(r'^login$', currency.views.loginPage),
    url(r'^logout', currency.views.logoutPage),
    url(r'^register$', currency.views.registerPage),
    url(r'^index$',currency.views.webIndex),
    url(r'^$',currency.views.webIndex),

    # 相册页面
    url(r'^album$', album.views.albumContent),
    url(r'^album/$', album.views.albumContent),

    # 视频页面
    url(r'^video$', video.views.videoContent),
    url(r'^video/$', video.views.videoContent),
    # 简历页面
    url(r'^resume$', resume.views.resumeIndex),
    url(r'^resume/$', resume.views.resumeIndex),

    # 项目页面
    url(r'^project$', myproject.views.projectContent),
    url(r'^project/$', myproject.views.projectContent),

    # 博客页面
    url(r'^blog$', blog.views.blogIndex),
    url(r'^blog/$', blog.views.blogIndex),
    url(r'^blog/index$', blog.views.blogIndex),
    url(r'^blog/list$', blog.views.blogList),
    url(r'^blog/content$', blog.views.blogArticle),
    # url(r'^blog/timeline$', blog.views.blogTimeline),

    # 用户
    url(r'^usercenter$', usercenter.views.userIndex),
    url(r'^usercenter/index', usercenter.views.userIndex),
    url(r'^usercenter/infor$', usercenter.views.userInfor),
    url(r'^usercenter/api$', usercenter.views.userAPI),


    # API
    url(r'^api$', apicenter.views.apiAuth),


    url(r'^uecontroller$', tools.ueditor.views.uecontroller),
    url(r'^files/(?P<path>.*$)', static.serve, {'document_root': settings.MEDIA_ROOT, }),
    url(r'^static/(?P<path>.*$)', static.serve, {'document_root': settings.STATIC_ROOT, }),
]

# urlpatterns += [
#     url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT,})
# ]
