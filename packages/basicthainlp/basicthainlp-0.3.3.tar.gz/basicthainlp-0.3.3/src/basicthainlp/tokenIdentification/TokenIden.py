import re
import os
import glob
from pathlib import Path
import re
class TokenIden(object):
    def __init__(self):
        self.otherSymb = r'[^\w\s\u002A\u002B\u002D/%<=>.,;]'
        self.mathSymb = r'[\u002A\u002B\u002D/%<=>]'
        self.punc = r'[.,;]'

        # self.th_char = '[\u0E01-\u0E5B]+'
        self.th_char = r'[\u0E01-\u0E4F]+'
        # self.th_con = r'[\u0E01-\u0E2E]+'
        self.th_mym = r'\u0E46'
        # self.th_digit = r'[\u0E50-\u0E59]+'

        self.en_char = r'[a-zA-Z]+'
        # self.en_digit = r'[0-9]+'

        # self.digit = r'\d+'
        self.digit = r'[-]?\d+([,]?\d{3})+([.]\d+)?|[-]?\d+[.]?\d+|[-]?\d+'
        self.order = r'\d+[.]\B'
        
        self.url = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
        self.email  = r'\S+@\S+'

        self.whitespace = r'\s'
        self.space = r' '    
        self.newline = r'[\r\n]'
        self.condList = [
            ['otherSymb',self.otherSymb] ,['mathSymb',self.mathSymb] ,['punc',self.punc],
            ['th_char',self.th_char] ,['th_mym',self.th_mym] ,
            ['en_char',self.en_char] , ['digit',self.digit] , ['order',self.order], 
            ['url',self.url], ['email',self.email],
            ['whitespace',self.whitespace] ,['space',self.space] ,['newline',self.newline]
        ]
    def listTag(self):
        for tag in self.condList:
            print(tag[0])    
    def replaceTag(self,listRep,textTokenList,tagList):
        newTokenList = textTokenList[:]
        for repArray in listRep:
            tag,rep = repArray.split('=')
            for i in range(len(tagList)):
                if tag == tagList[i]:
                    newTokenList[i] = rep
        return newTokenList
    def searchKey(self,key,text):
        return True if re.search(key, text) != None else False
    def search2List(self,key,text):
        indList = []
        resList = []
        for match in re.finditer(key, text):
            indList.append([match.start(), match.end()])
            resList.append(text[match.start():match.end()])
        return indList,resList
    def tagTokenIden(self,text):
        tokenIdenList = ['O:none' for x in range(len(text))]	
        for cond in self.condList:
            indList,resList = self.search2List(cond[1],text)
            for indArr in indList:
                tokenIdenList[indArr[0]] = 'B:'+cond[0]
                for i in range(indArr[0]+1,indArr[1]):
                    tokenIdenList[i] = 'I:'+cond[0]
        return tokenIdenList
    def toTokenList(self,text,tokenIdenList):
        textTokenList = []
        tagList = []
        preTag = ''
        tokenStr = ''
        for c, t in zip(text, tokenIdenList):
            if t[0] == 'B' or t[0] == 'O' or preTag != t[2:]:
                if tokenStr != '':
                    textTokenList.append(tokenStr)
                    tagList.append(preTag)
                tokenStr = c
            else:
                tokenStr += c
            preTag = t[2:]
        if tokenStr != '':
            textTokenList.append(tokenStr)
            tagList.append(preTag)
        return textTokenList,tagList

class DictToken(object):
    def __init__(self):
        self.dictList = []
    def readFile_short(self,inputFile):
        listTmp = [Path(os.path.basename(inputFile)).stem]
        with open(inputFile,'r') as fr:
            for line in fr:
                # print(line.rstrip('\r\n'))
                listTmp.append(line.rstrip('\r\n'))
        self.dictList.append(listTmp)   
    def readFloder(self,floderName):
        files=glob.glob(floderName+'/*')
        for fileName in files:     
            # print ("fileName = " + Path(os.path.basename(fileName)).stem)
            # print ("fileName = " + fileName)
            self.readFile_short(fileName)
    def find_all(self,sent,key):
        resList = []
        for ind in range(len(sent)):
            if sent[ind:ind+(len(key))] == key:
                resList.append(ind)
        return resList
    def repToken(self,begin,end,tagName,tokenIdenList):
        if end > begin:
            tokenIdenList[begin] = 'B:'+tagName
            for i in range(begin+1,end):
                tokenIdenList[i] = 'I:'+tagName
            if end < len(tokenIdenList):
                tokenIdenList[end] = 'B:'+tokenIdenList[end][2:]
        return tokenIdenList
    def rep_dictToken(self,sent,tokenIdenList):
        for listWord in self.dictList:
            for word_rep in listWord[1:]:
                indList = self.find_all(sent,word_rep)
                for ind in indList:
                    # print(word_rep,indList)
                    if ind > -1:
                        tokenIdenList = self.repToken(ind,ind+len(word_rep),listWord[0],tokenIdenList)
        return tokenIdenList

# textTest = "the 1..  .25 \"(12,378.36 / -78.9%) = 76,909\tcontain iphone 13 45. +-*/ -5 12.10.226.38.25 กค. สิงหา%/<=>  6 's\n"
# TID = TokenIden()
# tokenIdenList = TID.tagTokenIden(textTest)

# DTK = DictToken()
# DTK.readFloder('input')
# tokenIdenList = DTK.rep_dictToken(textTest,tokenIdenList)
# textTokenList,tagList = TID.toTokenList(textTest,tokenIdenList)
# for x, y in zip(textTokenList, tagList):
#     if y != 'otherSymb' and y != 'space':
#         print(x,y)