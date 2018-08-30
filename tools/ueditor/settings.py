# coding:utf-8
from django.conf import settings as gSettings  # 全局设置

# 工具栏样式，可以添加任意多的模式
TOOLBARS_SETTINGS = {
    "besttome": [
        ['fullscreen', 'source', '|', 'undo', 'redo', '|', 'bold', 'italic', 'underline', 'fontborder', 'strikethrough',
         'superscript', 'subscript', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|',
         'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', 'cleardoc', '|',
         'rowspacingtop', 'rowspacingbottom', '|', 'lineheight', 'pagebreak', 'template', 'background', '|', 'preview',
         'searchreplace', 'help', '|', 'paragraph', 'fontfamily', 'fontsize', '|', 'directionalityltr',
         'directionalityrtl', 'indent', '|', 'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|',
         'touppercase', 'tolowercase', '|', 'link', 'unlink', 'anchor', '|', 'imagenone', 'imageleft', 'imageright',
         'imagecenter', '|', 'insertimage', 'attachment', 'scrawl', 'emotion', 'map', 'gmap', 'insertframe',
         'insertcode', '|', 'horizontal', 'date', 'time', 'spechars', 'wordimage', '|', 'inserttable', 'deletetable',
         'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright',
         'mergedown', 'splittocells', 'splittorows', 'splittocols']],
    "mini": [['source', '|', 'undo', 'redo', '|', 'bold', 'italic', 'underline', 'formatmatch', 'autotypeset', '|',
              'forecolor', 'backcolor', '|', 'link', 'unlink', '|', 'simpleupload', 'attachment']],
    "normal": [['source', '|', 'undo', 'redo', '|', 'bold', 'italic', 'underline', 'removeformat', 'formatmatch',
                'autotypeset', '|', 'forecolor', 'backcolor', '|', 'link', 'unlink', '|', 'simpleupload', 'emotion',
                'attachment', '|', 'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow',
                'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows',
                'splittocols']]
}

# 默认的Ueditor设置，请参见ueditor.config.js
UEditorSettings = {
    "toolbars": TOOLBARS_SETTINGS["normal"],
    "autoFloatEnabled": False,
    # "defaultFileFormat":"%(basename)s_%(datetime)s_%(rnd)s.%(extname)s",   #默认保存上传文件的命名方式
    "defaultFileFormat": "%(datetime)s_%(rnd)s.%(extname)s",
# 默认保存上传文件的命名方式（时间_随机数.扩展名），由于apache常常出现字符不兼容问题，建议不要用中文的字样为好。
    "defaultSubFolderFormat": "blog/%(year)s%(month)s",
}
# 请参阅php文件夹里面的config.json进行配置
UEditorUploadSettings = {
    # 上传图片配置项
    "imageActionName": "uploadimage",  # 执行上传图片的action名称
    "imageMaxSize": 10485760,  # 上传大小限制，单位B,10M
    "imageFieldName": "upfile",  # * 提交的图片表单名称 */
    "imageUrlPrefix": "",
    "imagePathFormat": "",
    "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],  # 上传图片格式显示

    # 上传照片配置项
    "photoActionName": "uploadphoto",  # 执行上传图片的action名称
    "photoMaxSize": 10485760,  # 上传大小限制，单位B,10M
    "photoFieldName": "upfile",  # * 提交的图片表单名称 */
    "photoUrlPrefix": "",
    "photoPathFormat": "",
    "photoAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],  # 上传图片格式显示

    # 涂鸦图片上传配置项 */
    "scrawlActionName": "uploadscrawl",  # 执行上传涂鸦的action名称 */
    "scrawlFieldName": "upfile",  # 提交的图片表单名称 */
    "scrawlMaxSize": 10485760,  # 上传大小限制，单位B  10M
    "scrawlUrlPrefix": "",
    "scrawlPathFormat": "",

    # 截图工具上传 */
    "snapscreenActionName": "uploadimage",  # 执行上传截图的action名称 */
    "snapscreenPathFormat": "",
    "snapscreenUrlPrefix": "",

    # 抓取远程图片配置 */
    "catcherLocalDomain": ["127.0.0.1", "localhost", "img.baidu.com"],
    "catcherPathFormat": "",
    "catcherActionName": "catchimage",  # 执行抓取远程图片的action名称 */
    "catcherFieldName": "source",  # 提交的图片列表表单名称 */
    "catcherMaxSize": 10485760,  # 上传大小限制，单位B */
    "catcherAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],  # 抓取图片格式显示 */
    "catcherUrlPrefix": "",
    # 上传视频配置 */
    "videoActionName": "uploadvideo",  # 执行上传视频的action名称 */
    "videoPathFormat": "",
    "videoFieldName": "upfile",  # 提交的视频表单名称 */
    "videoMaxSize": 102400000,  # 上传大小限制，单位B，默认100MB */
    "videoUrlPrefix": "",
    "videoAllowFiles": [
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid"],  # 上传视频格式显示 */

    # 上传文件配置 */
    "fileActionName": "uploadfile",  # controller里,执行上传视频的action名称 */
    "filePathFormat": "",
    "fileFieldName": "upfile",  # 提交的文件表单名称 */
    "fileMaxSize": 204800000,  # 上传大小限制，单位B，200MB */
    "fileUrlPrefix": "",  # 文件访问路径前缀 */
    "fileAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml",".py",".c",".java",".m",".js","html",".log",'.csv'
    ],  # 上传文件格式显示 */

    # 列出指定目录下的图片 */
    "imageManagerActionName": "listimage",  # 执行图片管理的action名称 */
    "imageManagerListPath": "",
    "imageManagerListSize": 30,  # 每次列出文件数量 */
    "imageManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],  # 列出的文件类型 */
    "imageManagerUrlPrefix": "",  # 图片访问路径前缀 */

    # 列出指定目录下的文件 */
    "fileManagerActionName": "listfile",  # 执行文件管理的action名称 */
    "fileManagerListPath": "",
    "fileManagerUrlPrefix": "",
    "fileManagerListSize": 30,  # 每次列出文件数量 */
    "fileManagerAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".psd"
                                                         ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg",
        ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml",
        ".exe", ".com", ".dll", ".msi",'.csv'
    ]  # 列出的文件类型 */
}


# 更新配置：从用户配置文件settings.py重新读入配置UEDITOR_SETTINGS,覆盖默认
def UpdateUserSettings():
    UserSettings = getattr(gSettings, "UEDITOR_SETTINGS", {}).copy()
    if "config" in UserSettings:
        UEditorSettings.update(UserSettings["config"])
    if "upload" in UserSettings:
        UEditorUploadSettings.update(UserSettings["upload"])


# 读取用户Settings文件并覆盖默认配置
UpdateUserSettings()