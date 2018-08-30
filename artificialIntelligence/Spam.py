# 总体思路就是:分词-----计算TF-IDF权重-----选用模型预测

import re
import jieba.posseg as pseg
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression

class SpamHandle:
    def __init__(self,content):
        self.content = "".join(re.findall("[^\x00-\xff]",content))

    def getSpam(self):
        '''
        0 表示垃圾信息，1 表示正常信息
        :return:
        '''

        if len(self.content) <= 1:
            return 0

        # 从磁盘读取y原始数据进行训练
        X = []
        Y1 = []
        Y2 = []
        #
        f = open('artificialIntelligence/spamData/train.txt')
        for v in f:
            X.append([v.strip('\n').split('/')[0], v.strip('\n').split('/')[1]])  # strip('\n')是去除换行符\n
        f.close()

        # 进行分词，分词后保存在Y中
        for i in range(len(X)):
            words = pseg.cut(X[i][1])
            str1 = ""
            for key in words:
                str1 += key.word
                str1 += ' '
            Y1.append(str1)  # 短信内容
            Y2.append(X[i][0])  # 是否是垃圾的标志

        # 将样本分为训练集和测试集
        x_train_Chinese, x_test_Chinese, y_train, y_test = train_test_split(Y1, Y2, train_size=0.99)

        # 通过TfidfVectorizer算出TF-IDF权重
        vectorizer = TfidfVectorizer()
        x_train = vectorizer.fit_transform(x_train_Chinese)

        '''
        #模块一:测试准确率，召回率等信息表
        #核心代码
        classifier=LogisticRegression()
        classifier.fit(x_train,y_train)
        y_tanin_predict=classifier.predict(x_train)
        
        print(metrics.classification_report(y_train,y_tanin_predict))       #包含准确率，召回率等信息表
        print(metrics.confusion_matrix(y_train,y_tanin_predict))            #混淆矩阵
        '''

        # 模块二:预测信息
        # 读取待预测的短息读取到X1中


        X1 = self.content

        # 进行分词，分词后保存在X2中

        words = pseg.cut(X1)
        str1 = ""
        for key in words:
            str1 += key.word
            str1 += ' '
        X2 = [str1]  # 短信内容

        # 计算待预测短息的TF-IDF权重
        x_demand_prediction = vectorizer.transform(X2)

        # 预测
        classifier = LogisticRegression()
        classifier.fit(x_train, y_train)
        y_predict = classifier.predict(x_demand_prediction)


        if int(y_predict[0]) == 0:
            return 1
        else:
            return 0