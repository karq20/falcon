#!/usr/bin/env python
import os.path
import json
import sys
import pytesseract
import re
import difflib
import csv
import text_with_confidence
from copy import copy
from PIL import Image
import fast


# Run text_with_confidence X times with rgb = rgb + y and Y times with confidence c = c + d

def get():

    # 9 sec with multithreading
    image_list = ['./test/data/pan/mohitpan.jpg', './test/data/pan/lokeshpan.jpg', './test/data/pan/randompancard.jpg', './test/data/pan/randompancard2.jpg']
    no_of_proc = 4
    lines = fast.process(image_list, 90, 40, no_of_proc)
    return lines

print(get())

"""
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


# Read Database
with open('namedb.csv', 'r') as f:
    reader = csv.reader(f)
    newlist = list(reader)
newlist = sum(newlist, [])

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
except Exception as ex:
    pass

try:
    fathername = textlist2[0]
    textlist2.remove(fathername)
except Exception as ex:
    pass

try:
    dobt = textlist2[0]
    textlist2.remove(dobt)
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


# Making tuples of data
data = {}
data['Name'] = name
data['Father Name'] = str(fathername)
data['Date of Birth'] = str(dobt)
data['PAN'] = str(panno)

print('------------------------------------- PARSED PAN OUTPUT ----------------------------------------------------')
print(data)
print('------------------------------------------------------------------------------------------------------------')

# Writing data into JSON
with open('../result/' + os.path.basename(sys.argv[1]).split('.')[0]
          + '.json', 'w') as fp:
    json.dump(data, fp)


# Removing dummy files
os.remove('temp.png')


# Reading data back JSON(give correct path where JSON is stored)
with open('../result/'+os.path.basename(sys.argv[1]).split('.')[0]
          + '.json', 'r') as f:
     ndata = json.load(f)

"""
