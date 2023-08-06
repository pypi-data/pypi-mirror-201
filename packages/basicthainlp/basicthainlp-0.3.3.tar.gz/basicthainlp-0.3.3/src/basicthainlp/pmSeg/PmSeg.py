import sklearn_crfsuite
import numpy as np
import os
THIADIR, THISFILENAME = os.path.split(__file__)
class PmSeg(object):
    def __init__(self):
        self.pmDef = None
        self.pmCrf = None
    def init_cls(self,inputFile_def=os.path.join(THIADIR, "input/thaiSylseg.def"),
                 inputFile_model=os.path.join(THIADIR, "output/pm_crf.model")):
        self.pmDef = self.loadDef(inputFile_def)
        self.pmCrf = self.loadModel(inputFile_model)
    def status_cls(self):
        if self.pmDef == None or self.pmCrf == None:
            return False
        else:
            return True 
    def loadDef(self,inputFile):
        def_dict = {}
        with open(inputFile,'r') as fr:
            for line in fr:
                strLine = line.rstrip('\r\n')
                lineArr = strLine.split(':')
                if len(lineArr) == 3:
                    aphList = lineArr[2].strip('{}').split(',')
                    for aph in aphList:
                        def_dict[aph] = lineArr[1]
        return def_dict
    def loadModel(self,inputFile):
        return sklearn_crfsuite.CRF(model_filename=inputFile)

    def mapAph(self,key):
        if key in self.pmDef.keys():
            return self.pmDef[key]
        else:
            return self.pmDef['other']

    def getColumn(self,matrix, i):
        return [row[i] for row in matrix]

    def word2features(self,sent, i):
        windows_size = 4
        features = {
            'bias': 1.0,
            'word': sent[i][0],
            'postag': sent[i][1],
        }
        if i == 0:
            features['BOS'] = True
        if i == len(sent)-1:
            features['EOS'] = True
        for x in range(1,windows_size):
            if i > x-1:
                features.update({
                '-'+str(x)+':word': sent[i-x][0],
                '-'+str(x)+':postag': sent[i-x][1],
                '-'+str(x)+':word[-'+str(x)+':]': ''.join(self.getColumn(sent[i-x:i+1], 0)),
            })
            if i+x < len(sent)-2:
                features.update({
                    '+'+str(x)+':word': sent[i+x][0],
                    '+'+str(x)+':postag': sent[i+x][1],
                    '+'+str(x)+':word[:'+str(x+1)+']': ''.join(self.getColumn(sent[i:i+x+1], 0)),
                })
        return features

    def sent2features(self,sent):
        return [self.word2features(sent, i) for i in range(len(sent))]
    def sent2labels(self,sent):
        return [label for token, postag, label in sent]


    def word2DataList(self,sent):
        aphList = []
        for c in sent:
            aphList.append([c,self.mapAph(c)])
        return aphList
    def dataList2pmSeg(self,dataList):
        s_test = np.array([self.sent2features(dataList)])
        return self.pmCrf.predict(s_test)
    def pmSeg2List(self,sentList,pmSegList):
        pmList = []
        prePm = ''
        for s,w in zip(sentList,pmSegList):
            if w == 'B' or w == 'BA':
                if prePm != '':
                    pmList.append(prePm)
                    prePm = ''
                prePm += s
            else:
                prePm += s
        if prePm != '':
            pmList.append(prePm)
        return pmList
    def pmSeg2dataTagList(self,wordList,tagList):
        pmList = []
        prePm = []
        for (w,c),t in zip(wordList,tagList):
            if t == 'B' or t == 'BA':
                if prePm != []:
                    pmList.append(prePm)
                    prePm = []
                prePm.append([w,c,t])
            else:
                prePm.append([w,c,t])
        if prePm != []:
            pmList.append(prePm)
        return pmList
    
# textTest = 'รัฐราชการ'
# ps = PmSeg('input/thaiSylseg.def','output/pm_crf.model')
# data_list = ps.word2DataList(textTest)
# print(data_list)
# pred = ps.dataList2pmSeg(data_list)
# print(list(textTest))
# print(pred[0])
# print(ps.pmSeg2List(list(textTest),pred[0]))

