# 人工智能播客系统

## 前言
感谢各位小伙伴关注我的Github，本项目是我博客的源代码，我的博客是使用Django实现，融入了大量人工智能的元素。

## 使用方法
* 找到package列表文件（package列表.txt），确定服务器安装了对应的Package以及对应的版本；
* 将本系统放入服务器中，找到BlogSystem/base.conf文件，配置数据库等信息；
* 同步数据库，并打开页面：/register，进行账号注册，系统默认uid=1的为admin；
* 打开管理员后台：/admin，进行其他信息配置，例如邮箱信息配置，网站Seo等信息配置；
* 由于Git对文将上传有100M大小的限制，所以您还需要去Google上面找两个模型文件resnet50_coco_best_v2.0.1.h5与resnet50_weights_tf_dim_ordering_tf_kernels.h5，下载之后放在/tools/imageAI中即可；
* 此时完成了整个项目的配置，可以正常使用；

## 博客亮点
* 本博客采用了自动文本摘要和关键词提取技术，您发送文章之后，系统会自动提取关键词和摘要，并对应放入keyword和description中，实现SEO优化；
* 用户发送垃圾留言，本系统可以进行初步判断，并且识别恶意留言，禁止发送；
* 博文搜索功能不是简单地关键字匹配，而是通过了自然语言处理，进行了相关性检测，相对来说更智能；
* 本系统提供IP限制功能，用户可以确定IP最大访问次数，这样可以确定每个IP，每天访问最多次数；
* 本系统拥有两套后台，分别是普通用户后台和管理员后台，普通用户后台是/usercenter，管理员后台是/admin；
* 本系统可以提供自定义模板，具体的模板规则，以后有时间，我会慢慢提供，自定义模板设置方法是在/admin中设置；
* 提供大量随机功能，例如可以自设定简历模板，以及首页背景图，也就是说，每次打开首页或者模板页面，否是不同样式的，提供新鲜感；
* 拥有项目中心、视频中心、相册中心等众多功能；

## 关于作者
* 姓名：刘宇
* 邮箱：service@52exe.cn
* 介绍：我是一个活泼开朗，热爱旅游的程序员，虽然是跨专业被保送浙大读研，虽然在某些基础知识上可能不如 计算机专业出身的小伙伴，但是在同年级中我的开发经验和我对问题的思考能力，解决能力以及创新能力、学习能力、应用能力等却都是排在前列的。因为挚爱计算机和想去异国看看科技发展情况，通过自身努力得到了韩国江源大学的公费交换名额；因为自己自学编程时更多在用手机查一些资料，创新性的建立了Anycodes 在线编程平台，经网友互传其手机APP 累计下载量高达22 万次；因为要面试了，自己做了一个微信小程序（程序员题库）来满足自己和周边人面试刷题的小需求；不断地将学习到的知识注入到实践中，通过Sklearn 等技术，为自己的博客增加了自动摘要和关键词提取技术，将爬虫技术和微信公众号开发结合，建立了校园一点通信息平台，使同学们可以通过该平台查看课表，成绩，通知等。同时自己也多次参加数学建模竞赛，创业比赛均获得过国家级奖项，参加过天池大数据比赛和CCF 大数据比赛，也多次进过百强。我始终相信，自己的能力和付出的努力成正比，通过不断提高自己的开发经验，不断完善自己的基础知识，我相信，脚踏实地的自己一定会有所收获。


## 功能展示

* 首页展示
![首页展示](https://github.com/anycodes/BlogSystem/blob/master/descPic/1.png?raw=true)
* 博客首页
![博客首页](https://github.com/anycodes/BlogSystem/blob/master/descPic/2.png?raw=true)
* 博客内容页
![博客内容页](https://github.com/anycodes/BlogSystem/blob/master/descPic/3.png?raw=true)
* 简历页面
![简历页面](https://github.com/anycodes/BlogSystem/blob/master/descPic/4.png?raw=true)
* 相册页面
![相册页面](https://github.com/anycodes/BlogSystem/blob/master/descPic/5.png?raw=true)
* 视频中心
![视频中心](https://github.com/anycodes/BlogSystem/blob/master/descPic/6.png?raw=true)
* 项目中心
![项目中心](https://github.com/anycodes/BlogSystem/blob/master/descPic/7.png?raw=true)
* 用户后台首页
![用户后台首页](https://github.com/anycodes/BlogSystem/blob/master/descPic/8.png?raw=true)
* 用户后台API页面
![用户后台API页面](https://github.com/anycodes/BlogSystem/blob/master/descPic/9.png?raw=true)
* 管理员后台文章列表
![管理员后台文章列表](https://github.com/anycodes/BlogSystem/blob/master/descPic/10.png?raw=true)
* 管理员后台发布文章
![管理员后台发布文章](https://github.com/anycodes/BlogSystem/blob/master/descPic/11.png?raw=true)



