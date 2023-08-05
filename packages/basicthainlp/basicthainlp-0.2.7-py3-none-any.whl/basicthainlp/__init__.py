from .pmSeg import PmSeg
from .tokenIdentification import TokenIden, DictToken

def get_ps(TID=TokenIden(),DTK=DictToken(),PS=PmSeg(),textInput="ทดสอบ"):
  tokenIdenList = TID.tagTokenIden(textInput)
  tokenIdenList = DTK.rep_dictToken(textInput,tokenIdenList)
  textTokenList,tagList = TID.toTokenList(textInput,tokenIdenList)
  # ['otherSymb','mathSymb','punc','th_char','th_mym','en_char','digit','order','url','whitespace','space','newline','abbreviation','ne']
  # newTokenList = TID.replaceTag(['digit=<digit>'],textTokenList,tagList)
  newTokenList = []
  for textToken, tag in zip(textTokenList, tagList):
      if tag == 'th_char':
          data_list = PS.word2DataList(textToken)
          pred = PS.dataList2pmSeg(data_list)
          psList = PS.pmSeg2List(list(textToken),pred[0])
          newTokenList.extend(psList)
      else:
          newTokenList.append(textToken)
  return newTokenList