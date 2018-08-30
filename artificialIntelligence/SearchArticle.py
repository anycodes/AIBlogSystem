import os.path
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
from whoosh.query import *
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer

class SearchArticleHandle:
    def __init__(self,articleList):
        analyzer = ChineseAnalyzer()
        self.schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True, analyzer=analyzer), path=ID(stored=True), tags=KEYWORD, icon=STORED)
        if not os.path.exists("cache"):
            os.mkdir("cache")
        self.ix = create_in("cache", self.schema)
        self.ix = open_dir("cache")
        self.writer = self.ix.writer()
        for eveArticle in articleList:
            self.writer.add_document(title=str(eveArticle[0]), content=str(eveArticle[1]),path=str(eveArticle[2]))
        self.writer.commit()

    def getResult(self,searchStr):
        with self.ix.searcher() as searcher:
            parser = QueryParser("content", self.ix.schema)
            myquery = parser.parse(searchStr)
            results = searcher.search(myquery)
            resultData = []
            for eveResult in results:
                resultData.append(eveResult["path"])
        return resultData