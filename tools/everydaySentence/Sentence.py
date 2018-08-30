import random

class Sentence:
    def __init__(self):
        self.path = "files/system/everydaySentence.data"

    def getAll(self):
        with open(self.path) as f:
            readData = f.readlines()

        return readData

    def getOneSentence(self,lanminNum=10, lenmaxNum=35):
        sentenceData = self.getAll()
        while True:
            onSentence = random.choice(sentenceData)
            if len(onSentence) >= lanminNum and len(onSentence) <= lenmaxNum:
                break
        sentence,author = onSentence.split("----")
        return (sentence.strip(),author.strip())