import re
import math
import jieba
import jieba.analyse
import numpy as np
import networkx as nx
import random


class ArticleHandle:
    def __init__(self, article):
        self.article = "".join(re.findall("[^\x00-\xff]",article))
        
    def split_sentences(self, full_text):
        sents = re.split(u'[\n。]', full_text)
        sents = [sent for sent in sents if len(sent) > 0]  # 去除只包含\n或空白符的句子
        return sents

    def cal_sim(self, wordlist1, wordlist2):
        """
        给定两个句子的词列表，计算句子相似度。计算公式参考Textrank论文
        :param wordlist1:
        :param wordlist2:
        :return:
        """
        co_occur_sum = 0
        wordset1 = list(set(wordlist1))
        wordset2 = list(set(wordlist2))
        for word in wordset1:
            if word in wordset2:
                co_occur_sum += 1.0
        if co_occur_sum < 1e-12:  # 防止出现0的情况
            return 0.0
        denominator = math.log(len(wordset1)) + math.log(len(wordset2))
        if abs(denominator) < 1e-12:
            return 0.0
        return co_occur_sum / denominator

    def text_rank(self, sentences, num=10, pagerank_config={'alpha': 0.85, }):
        """
        对输入的句子进行重要度排序
        :param sentences: 句子的list
        :param num: 希望输出的句子数
        :param pagerank_config: pagerank相关设置，默认设置阻尼系数为0.85
        :return:
        """
        sorted_sentences = []
        sentences_num = len(sentences)
        wordlist = []  # 存储wordlist避免重复分词，其中wordlist的顺序与sentences对应
        for sent in sentences:
            tmp = []
            cur_res = jieba.cut(sent)
            for i in cur_res:
                tmp.append(i)
            wordlist.append(tmp)
        graph = np.zeros((sentences_num, sentences_num))
        for x in range(sentences_num):
            for y in range(x, sentences_num):
                similarity = self.cal_sim(wordlist[x], wordlist[y])
                graph[x, y] = similarity
                graph[y, x] = similarity
        nx_graph = nx.from_numpy_matrix(graph)
        scores = nx.pagerank(nx_graph, **pagerank_config)  # this is a dict
        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        for index, score in sorted_scores:
            item = {"sent": sentences[index], 'score': score, 'index': index}
            sorted_sentences.append(item)
        return sorted_sentences[:num]

    def extract_abstracts(self, full_text, sent_num=5):
        """
        摘要提取的入口函数，并根据textrank结果进行摘要组织
        :param full_text:
        :param sent_num:
        :return:
        """
        sents = self.split_sentences(full_text)
        trank_res = self.text_rank(sents, num=sent_num)
        sorted_res = sorted(trank_res, key=lambda x: x['index'], reverse=False)
        return sorted_res

    # 对外开放的获取摘要的接口
    def getAbstract(self,sent_num = random.randint(3, 6)):
        res = self.extract_abstracts(self.article, sent_num=sent_num)
        content = ""
        for eve_content in res:
            content = content + eve_content["sent"]
        return content.strip()

    # 对外开放的获取关键词接口
    def getKeywords(self):
        # 引入TF-IDF关键词抽取接口
        tfidf = jieba.analyse.extract_tags
        # 基于TF-IDF算法进行关键词抽取
        keywords = tfidf(self.article)

        tempKeywords = []

        for eveKeyword in keywords:
            if len(eveKeyword) < 5 and len(tempKeywords) < 6:
                tempKeywords.append(eveKeyword)

        return tempKeywords