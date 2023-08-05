# Token Identification
## Example code TokenIden
```
from basicthainlp import TokenIden
TID = TokenIden()
textTest = "the 1..  .25 \"(12,378.36 / -78.9%) = 76,909\tcontain iphone 13 45. +-*/ -5 12.10.226.38.25 กค. สิงหา%/<=>  6 's\n"
tokenIdenList = TID.tagTokenIden(textTest)
textTokenList,tagList = TID.toTokenList(textTest,tokenIdenList)
for x, y in zip(textTokenList, tagList):
    if y != 'otherSymb' and y != 'space':
        print(x,y)
```
## Example code TokenIden: Add dict
input เป็น folder ที่ข้างในเป็นไฟล์ซึ่งเป็น list ของคำ 1 colum
Tag ที่ได้จะตรงกันชื่อไฟล์
### ตัวอย่าง dict
input
--abbreviation.txt #Tag ที่ได้ออกมีคือ abbreviation
----กค.
----สค.
----กพ.
```
from basicthainlp import TokenIden, DictToken
TID = TokenIden()
textTest = "the 1..  .25 \"(12,378.36 / -78.9%) = 76,909\tcontain iphone 13 45. +-*/ -5 12.10.226.38.25 กค. สิงหา%/<=>  6 's\n"
tokenIdenList = TID.tagTokenIden(textTest)
# >>> Add dict 
DTK = DictToken()
DTK.readFloder('input')
tokenIdenList = DTK.rep_dictToken(textTest,tokenIdenList)
# <<< Add dict
textTokenList,tagList = TID.toTokenList(textTest,tokenIdenList)
for x, y in zip(textTokenList, tagList):
    if y != 'otherSymb' and y != 'space':
        print(x,y)
```
================================================================================
# Word token to Pseudo Morpheme Segmentation
-ไม่ควรใช้งานกับประโยคภาษาไทยยาวๆ ควรตัดคำ หรือ ใช้งานรวมกับ TokenIdentification
## Example code PmSeg
```
from basicthainlp import PmSeg
ps = PmSeg()

textTest = 'รัฐราชการ'
data_list = ps.word2DataList(textTest)
print(data_list)
pred = ps.dataList2pmSeg(data_list)
print(list(textTest))
print(pred[0])
print(ps.pmSeg2List(list(textTest),pred[0]))
```
```
[['ร', 'Ccc'], ['ั', 'Vu'], ['ฐ', 'C'], ['ร', 'Ccc'], ['า', 'Vm'], ['ช', 'C'], ['ก', 'C'], ['า', 'Vm'], ['ร', 'Ccc']]
['ร', 'ั', 'ฐ', 'ร', 'า', 'ช', 'ก', 'า', 'ร']
['B', 'I', 'C', 'B', 'I', 'C', 'B', 'I', 'I']
['รัฐ', 'ราช', 'การ']
```
## Example code PmSeg: ใช้งานกับ Token Identification
```
from basicthainlp import PmSeg
from basicthainlp.tokenIdentification import TokenIden, DictToken
TID = TokenIden()
DTK = DictToken()
DTK.readFloder('input')
ps = PmSeg()
textTest = 'ติดตามข่าวล่าสุด 12 iphone'
tokenIdenList = TID.tagTokenIden(textTest)
tokenIdenList = DTK.rep_dictToken(textTest,tokenIdenList)
textTokenList,tagList = TID.toTokenList(textTest,tokenIdenList)
# ['otherSymb','mathSymb','punc','th_char','th_mym','en_char','digit','order','url','whitespace','space','newline','abbreviation','ne']
# newTokenList = TID.replaceTag(['digit=<digit>'],textTokenList,tagList)
newTokenList = []
for textToken, tag in zip(textTokenList, tagList):
    if tag == 'th_char':
        data_list = ps.word2DataList(textToken)
        pred = ps.dataList2pmSeg(data_list)
        psList = ps.pmSeg2List(list(textToken),pred[0])
        newTokenList.extend(psList)
    else:
        newTokenList.append(textToken)
print(newTokenList)
```