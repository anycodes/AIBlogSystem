import re

class Information:
    def __init__(self):

        with open("BlogSystem/base.conf") as f:
            readData = f.read()

        readData = readData.replace("\n","--==--==--==--").replace("\r\n","--==--==--==--")
        baseInformation = re.findall("<baseInformation>([\s\S]*)</baseInformation>", readData)[0].split("--==--==--==--")

        self.informationDict = {}

        for eveInformation in baseInformation:
            eveInformation = eveInformation.strip()
            if eveInformation and ":" in eveInformation:
                key, value = eveInformation.split(":", 1)
                self.informationDict[key] = value

    def getAll(self):
        return self.informationDict

    def getValue(self, key):
        return self.informationDict[key]

