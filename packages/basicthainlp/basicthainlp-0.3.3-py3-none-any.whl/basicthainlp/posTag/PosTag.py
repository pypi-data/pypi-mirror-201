import numpy as np
import sklearn_crfsuite
import os
from ..tokenIdentification import TokenIden, DictToken
from ..pmSeg import PmSeg
THIADIR, THISFILENAME = os.path.split(__file__)
class PosTag(object):
    def __init__(self):
       self.TID = None
       self.DTK = None
       self.PS = None
       self.crfModel = None
    def init_cls(self,tid_cls=TokenIden(),dtk_cls=DictToken(),ps_cls=PmSeg(),modelInput=os.path.join(THIADIR, "output/pos_crf.model")):
       self.TID = tid_cls
       self.DTK = dtk_cls
       self.PS = ps_cls
       self.crfModel = sklearn_crfsuite.CRF(model_filename=modelInput)
    def status_cls(self):
        if self.TID == None or self.DTK == None or self.PS == None or self.crfModel == None:
            return False
        else:
            return True 
    def get_ps(self,line):
        tokenIdenList = self.TID.tagTokenIden(line)
        tokenIdenList = self.DTK.rep_dictToken(line,tokenIdenList)
        textTokenList,tagList = self.TID.toTokenList(line,tokenIdenList)
            
        # ['otherSymb','mathSymb','punc','th_char','th_mym','en_char','digit','order','url','whitespace','space','newline','abbreviation','ne']
        # newTokenList = TID.replaceTag(['digit=<digit>'],textTokenList,tagList)
        newTokenList = []
        for textToken, tag in zip(textTokenList, tagList):
            # print(textToken,tag)
            if tag == 'th_char':
                data_list = self.PS.word2DataList(textToken)
                pred = self.PS.dataList2pmSeg(data_list)
                psList = self.PS.pmSeg2List(list(textToken),pred[0])

                newTokenList.extend(psList)
            else:
                newTokenList.append(textToken)
        return newTokenList
    def getColumn(self,matrix, i):
        return [row[i] for row in matrix]

    def word2features(self,sent, i):
        windows_size = 4
        features = {
            'bias': 1.0,
            'word': sent[i][0],
        }
        if i == 0:
            features['BOS'] = True
        if i == len(sent)-1:
            features['EOS'] = True
        for x in range(1,windows_size):
            if i > x-1:
                features.update({
                '-'+str(x)+':word': sent[i-x][0],
                '-'+str(x)+':word[-'+str(x)+':]': ''.join(self.getColumn(sent[i-x:i+1], 0)),
            })
            if i+x < len(sent)-2:
                features.update({
                    '+'+str(x)+':word': sent[i+x][0],
                    '+'+str(x)+':word[:'+str(x+1)+']': ''.join(self.getColumn(sent[i:i+x+1], 0)),
                })
        return features

    def sent2features(self,sent):
        return [self.word2features(sent, i) for i in range(len(sent))]
    def psSeg2WS(self,psList,posList):
        resWs = []
        resPos = []
        word = ''
        posTmp = ''
        for ps,pos in zip(psList,posList):
            if pos.startswith('B'):
                if word != '':
                    resWs.append(word)
                    resPos.append(posTmp)
                word = ps
                posTmp = pos[2:]
            else:
                word += ps
        if word != '':
            resWs.append(word)
            resPos.append(posTmp)
        return resWs,resPos
    def sent2DataList(self,psList):
        dataList = []
        for ps in psList:
            dataList.append([ps,'I'])
        return dataList
    def tagPOS(self,textInput):
        psTest_list = self.get_ps(textInput)
        s_test = np.array([self.sent2features(self.sent2DataList(psTest_list))])
        s_pred = self.crfModel.predict(s_test)
        return psTest_list,s_pred[0]

# import sys
# import os
# dir_token = "/opt/git/gitLab/aitoolpy/TokenIdentification/"
# dictToken = 'input/dictToken'
# sys.path.insert(0,dir_token )
# from TokenIden import TokenIden,DictToken

# TID = TokenIden()
# DTK = DictToken()
# DTK.readFloder(dictToken)

# dir_pm = "/opt/git/gitLab/aitoolpy/CRFSuite/pmSeg/"
# sys.path.insert(0,dir_pm)
# from PmSeg import PmSeg
# PS = PmSeg(os.path.join(dir_pm,'input/thaiSylseg.def'),os.path.join(dir_pm,'output/pm_crf.model'))

# textTest = 'จากนั้นคนร้ายก็ได้ขับมุ่งไปทางถนนเจริญกรุง' 
# pos_cls = PosTag(TID,DTK,PS,'output/pos_crf.model')
# ps_list,tag_list = pos_cls.tagPOS(textTest)
# print(ps_list)
# print(tag_list)
# word_list,pos_list = pos_cls.psSeg2WS(ps_list,tag_list)
# print(word_list)
# print(pos_list)