# Word token to Pseudo Morpheme Segmentation
-ไม่ควรใช้งานกับประโยคภาษาไทยยาวๆ ควรตัดคำ หรือ ใช้งานรวมกับ TokenIdentification
## Example code
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