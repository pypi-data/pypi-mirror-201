from .pmSeg import PmSeg
from .tokenIdentification import TokenIden, DictToken
from .posTag import PosTag
TID_OBj = TokenIden()
DTK_OBj = DictToken()
PS_OBj = PmSeg()
def get_ps(tid_cls=TID_OBj,dtk_cls=DTK_OBj,ps_cls=PS_OBj,textInput="ทดสอบ"):
    if ps_cls.status_cls() == False:
        ps_cls.init_cls()
    tokenIdenList = tid_cls.tagTokenIden(textInput)
    if dtk_cls != None:
        tokenIdenList = dtk_cls.rep_dictToken(textInput,tokenIdenList)
    textTokenList,tagList = tid_cls.toTokenList(textInput,tokenIdenList)
    # ['otherSymb','mathSymb','punc','th_char','th_mym','en_char','digit','order','url','whitespace','space','newline','abbreviation','ne']
    # newTokenList = tid_cls.replaceTag(['digit=<digit>'],textTokenList,tagList)
    newTokenList = []
    for textToken, tag in zip(textTokenList, tagList):
        if tag == 'th_char':
            data_list = ps_cls.word2DataList(textToken)
            pred = ps_cls.dataList2pmSeg(data_list)
            psList = ps_cls.pmSeg2List(list(textToken),pred[0])
            newTokenList.extend(psList)
        else:
            newTokenList.append(textToken)
    return newTokenList