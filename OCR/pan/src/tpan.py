#!/usr/bin/env python
import os
import os.path
import json
import sys
import pytesseract
import re
import difflib
import csv
from copy import copy

try:
    from PIL import Image
except Exception as ex:
    print ("please install PIL")
    sys.exit()
path = sys.argv[1]

img = Image.open(path)
img = img.convert('RGBA')
pix = img.load()

for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pix[x, y][0] < 100 or pix[x, y][1] < 100 or pix[x, y][2] < 100:
            pix[x, y] = (0, 0, 0, 255)
        else:
            pix[x, y] = (255, 255, 255, 255)

img.save('temp.png')

text = pytesseract.image_to_string(Image.open('temp.png'))
# text = pytesseract.image_to_string(img)

text = filter(lambda x: ord(x) < 128, text)
filterText = text
# filterText = "".join(t for t in text if t.isalnum() or t == '\n' or t.isspace() or t == '/')
# print("filtered output-\n" + filterText)


# Initializing data variable
name = None
fname = None
dob = None
pan = None
nameline = []
dobline = []
panline = []
text0 = []
text1 = []
text2 = []
govRE_str = '(GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT\
             |PARTMENT|ARTMENT|INDIA|NDIA|INCOME|NCOME|TAX|DEPT|GOVT)$'
numRE_str = '(Number|umber|Account|ccount|count|Permanent|\
             ermanent|manent)$'

# Searching for PAN
lines = filterText.split('\n')
for lin in lines:
    s = lin.strip()
    s = s.rstrip()
    s = s.lstrip()
    text1.append(s)

textlist = list(filter(None, text1))

lineno = 0

for text in textlist:
    xx = text.split()
    if ([w for w in xx if re.search(govRE_str, w)]):
        lineno = textlist.index(text)
        break

textlist = textlist[lineno+1:]
print(textlist)


# -----------Read Database
with open('namedb.csv', 'r') as f:
    reader = csv.reader(f)
    newlist = list(reader)
newlist = sum(newlist, [])

# Searching for Name and finding closest name in database
# try:
# 	text0 = filter(None, text0)
# 	for x in text0:
# 		for y in x.split( ):
# 			if(difflib.get_close_matches(y.upper(), newlist)):
# 				nameline.append(x)
# 				break
# 	name = ''.join(str(e) for e in nameline)
# except:
# 	pass

textlist2 = copy(textlist)
try:
    for text in textlist:
        for y in text.split():
            match = difflib.get_close_matches(y.upper(), newlist)
            if(match):
                nameline.append(match[0])
                textlist2.remove(text)
                break
except Exception as ex:
    pass

try:
    name = nameline[0]
    print(name)
except Exception as ex:
    pass

try:
    fathername = textlist2[0]
    print(fathername)
    textlist2.remove(fathername)
except Exception as ex:
    pass

try:
    dobt = textlist2[0]
    print(dobt)
    textlist2.remove(dobt)
    # print(textlist2)
except Exception as ex:
    pass

panno=''
try:
    for word in textlist2:
        word = word.replace(' ', '')
        if word.isalnum() and len(word) == 10:
                panno = word

except Exception as ex:
    pass

print(panno)

# Making tuples of data
data = {}
data['Data'] = textlist
data['Name'] = name
data['Father Name'] = fathername
data['Date of Birth'] = dobt
data['PAN'] = panno

# Writing data into JSON
with open('../result/' + os.path.basename(sys.argv[1]).split('.')[0]
          + '.json', 'w') as fp:
    json.dump(data, fp)


# Removing dummy files
# os.remove('temp.png')



# Reading data back JSON(give correct path where JSON is stored)
with open('../result/'+os.path.basename(sys.argv[1]).split('.')[0]
          + '.json', 'r') as f:
     ndata = json.load(f)


