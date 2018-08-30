from django.shortcuts import render
import random
from BlogSystem.information import Information
import resume.models
# Create your views here.

def resumeIndex(request):
    mobile = 1
    if "android" in str(request.META["HTTP_USER_AGENT"]).lower():
        mobile = 2
    if "iphone" in str(request.META["HTTP_USER_AGENT"]).lower():
        mobile = 2


    information = Information()
    totalInfor = information.getAll()

    moduleData = random.choice(resume.models.ResumeModel.objects.filter(keyData="template"))
    moduleDataTem = moduleData.valueData

    totalTempData = resume.models.ResumeModel.objects.all()
    totalData = {}
    haveKey = []
    for eveData in totalTempData:
        if eveData.keyData in haveKey:
            totalData[eveData.keyData].append(eveData.valueData)
        else:
            haveKey.append(eveData.keyData)
            totalData[eveData.keyData] = []
            totalData[eveData.keyData].append(eveData.valueData)


    return render(request, "resume/%s/index.html"%(moduleDataTem),locals())