# -*- coding: utf-8 -*-
from BlogSystem import settings
from tools.ueditor import settings as USettings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import urllib.parse
import datetime, random
from currency.models import FileModel
from album.models import ImagesModel


def get_output_path(request, path_format, fileformatdict):
    # 取得输出文件的路径
    OutputPathFormat = (
        request.GET.get(path_format, USettings.UEditorSettings["defaultFileFormat"]) % fileformatdict).replace("\\", "/")

    # 分解OutputPathFormat
    OutputFile = os.path.split(OutputPathFormat)[1]
    if not OutputFile:  # 如果OutputFile为空说明传入的OutputPathFormat没有包含文件名，因此需要用默认的文件名
        OutputFile = USettings.UEditorSettings["defaultFileFormat"] % fileformatdict
        OutputPathFormat = os.path.join(OutputPathFormat, OutputFile)
    subfolder = USettings.UEditorSettings['defaultSubFolderFormat'] % fileformatdict + '/'
    OutputPath = settings.MEDIA_ROOT + subfolder
    OutputPathFormat = subfolder + OutputPathFormat
    if not os.path.exists(OutputPath):
        os.makedirs(OutputPath)
    return (OutputPathFormat, OutputPath, OutputFile)


# 保存上传的文件
def save_upload_file(PostFile, FilePath):
    try:
        f = open(FilePath, 'wb')
        for chunk in PostFile.chunks():
            f.write(chunk)
    except Exception as E:
        f.close()
        return u"写入文件错误:" + E.message
    f.close()
    return u"SUCCESS"


# 涂鸦功能上传处理
@csrf_exempt
def save_scrawl_file(request, filename):
    import base64
    try:
        content = request.POST.get(USettings.UEditorUploadSettings.get("scrawlFieldName", "upfile"))
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(content))
        state = "SUCCESS"
    except Exception as E:
        state = "写入图片文件错误:%s" % E.message
    return state


@csrf_exempt
def UploadFile(request):
    """上传文件"""

    if not request.method == "POST":
        return HttpResponse(json.dumps(u"{'state:'ERROR'}"), content_type="application/javascript")

    state = "SUCCESS"
    action = request.GET.get("action")
    # 上传文件
    upload_field_name = {
        "uploadfile": "fileFieldName", "uploadimage": "imageFieldName",
        "uploadscrawl": "scrawlFieldName", "catchimage": "catcherFieldName",
        "uploadvideo": "videoFieldName", "uploadphoto": "photoFieldName",
    }
    UploadFieldName = request.GET.get(upload_field_name[action], USettings.UEditorUploadSettings.get(action, "upfile"))
    # 上传涂鸦，涂鸦是采用base64编码上传的，需要单独处理
    if action == "uploadscrawl":
        upload_file_name = "scrawl.png"
        upload_file_size = 0
    else:
        # 取得上传的文件
        print(UploadFieldName)
        req_file = request.FILES.get(UploadFieldName, None)
        if req_file is None:
            return HttpResponse(json.dumps(u"{'state:'ERROR'}"), content_type="application/javascript")
        upload_file_name = req_file.name
        upload_file_size = req_file.size

        # 取得上传的文件的原始名称
    upload_original_name, upload_original_ext = os.path.splitext(upload_file_name)

    # 文件类型检验
    upload_allow_type = {
        "uploadfile": "fileAllowFiles",
        "uploadimage": "imageAllowFiles",
        "uploadphoto": "photoAllowFiles",
        "uploadvideo": "videoAllowFiles"
    }

    if action in upload_allow_type:
        allow_type = list(request.GET.get(upload_allow_type[action],USettings.UEditorUploadSettings.get(upload_allow_type[action], "")))
        if not upload_original_ext.lower() in allow_type:
            state = u"服务器不允许上传%s类型的文件。" % upload_original_ext

            # 大小检验
    upload_max_size = {
        "uploadfile": "filwMaxSize",
        "uploadimage": "imageMaxSize",
        "uploadscrawl": "scrawlMaxSize",
        "uploadvideo": "videoMaxSize",
        "uploadphoto": "photoMaxSize",
    }
    max_size = int(
        request.GET.get(upload_max_size[action], USettings.UEditorUploadSettings.get(upload_max_size[action], 0)))
    if max_size != 0:
        from tools.ueditor.utils import FileSize
        MF = FileSize(max_size)
        if upload_file_size > MF.size:
            state = u"上传文件大小不允许超过%s。" % MF.FriendValue

            # 检测保存路径是否存在,如果不存在则需要创建
    upload_path_format = {
        "uploadfile": "filePathFormat",
        "uploadimage": "imagePathFormat",
        "uploadscrawl": "scrawlPathFormat",
        "uploadvideo": "videoPathFormat",
        "uploadphoto": "photoPathFormat",
    }

    FileFormatDict = {
        "year": datetime.datetime.now().strftime("%Y"),
        "month": datetime.datetime.now().strftime("%m"),
        "day": datetime.datetime.now().strftime("%d"),
        "date": datetime.datetime.now().strftime("%Y%m%d"),
        "time": datetime.datetime.now().strftime("%H%M%S"),
        "datetime": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        "rnd": random.randrange(100, 999)
    }
    fileformat = FileFormatDict
    fileformat.update({
        "basename": upload_original_name,
        "extname": upload_original_ext[1:],
        "filename": upload_file_name,
    })

    # 取得输出文件的路径
    OutputPathFormat, OutputPath, OutputFile = get_output_path(request, upload_path_format[action], fileformat)

    # 所有检测完成后写入文件
    if state == "SUCCESS":
        if action == "uploadscrawl":
            state = save_scrawl_file(request, os.path.join(OutputPath, OutputFile))
        else:
            # 保存到文件中，如果保存错误，需要返回ERROR
            state = save_upload_file(req_file, os.path.join(OutputPath, OutputFile))

            # 返回数据
    return_info = {
        'url': urllib.parse.urljoin(settings.MEDIA_URL, OutputPathFormat),  # 保存后的文件名称
        'original': upload_file_name,  # 原始文件名
        # 'original': 'aa',
        'type': upload_original_ext,
        'state': state,  # 上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
        'size': upload_file_size
    }

    from os.path import getctime, getsize
    import time

    if action == "uploadphoto":
        FileModel.objects.create(name=str(return_info["original"]).replace(str(return_info["type"]), ""),
                            file_add=str(return_info["url"]), type=str(return_info["type"]),
                            size=getsize(str(return_info["url"])[1:]),
                            date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(getctime(str(return_info["url"])[1:]))), category="photo")


    return_info['url'] = return_info['url'].replace("files/upload", "files")
    return HttpResponse(json.dumps(return_info, ensure_ascii=False), content_type="application/javascript")


@csrf_exempt
def uecontroller(req):
    if req.GET['action'] in 'uploadimage|uploadfile|uploadscrawl|uploadphoto':
        return UploadFile(req)
    elif req.GET['action'] == 'config':
        return HttpResponse(json.dumps(USettings.UEditorUploadSettings, ensure_ascii=False),content_type="application/javascript")
