import re
import pymorphy3

# pattern = r'[12].*[789]'
pattern = r'(?=.*6)(?=.*[12])'
# pattern = r'[12].*[789]'

if re.search(pattern, 'D6sd1sdaA'):
    print(True)
else:
    print(False)

sen ='брать (с собой)'
sen = re.sub(r'\(.*\)', '', sen).strip()

morph = pymorphy3.MorphAnalyzer()
p = morph.parse(sen)
for x in p:
    if x.tag.POS == 'INFN':
        if x.tag.transitivity == 'tran':
            transitivityRu = 'Переходный'
        else:
            transitivityRu = 'Непереходный'
        break
    else:
        print(x)
        transitivityRu = ''
print(transitivityRu)