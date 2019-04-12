#!/usr/bin/env python
import os
import os.path
import json
import sys
import string
import pytesseract
import re
import difflib
import csv
import nltk
import subprocess
import dateutil.parser as dparser
from dateutil.parser import _timelex, parser
from PIL import Image, ImageEnhance, ImageFilter
path = sys.argv[1]
# path = "/Users/mohit/Downloads/aadhar.jpg"


img = Image.open(path)
img = img.convert('RGBA')
# img = img.filter(ImageFilter.SHARPEN)
pix = img.load()

# cropping
for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
            pix[x, y] = (0, 0, 0, 255)
        else:
            pix[x, y] = (255, 255, 255, 255)

img.save('processed.jpg')

# Call tesseract for orig image and sharpened image
subprocess.call("tesseract "+path+" original_text ", shell=True)
subprocess.call("tesseract processed.jpg processed_text ", shell=True)

original_text_file = open('original_text.txt', 'r')
original_text = original_text_file.read()
processed_text_file = open('processed_text.txt', 'r')
processed_text = processed_text_file.read()

text = filter(lambda x: ord(x)<128,original_text)
texttemp = filter(lambda x: ord(x)<128,processed_text)

# Initializing data variable
name = None
gender = None
year = None
uid = None
yearline = []
genline = []
nameline = []
text1 = []
text2 = []

# Searching for Year of Birth
lines = texttemp

for wordlist in lines.split('\n'):
    xx = wordlist.split( )
    if [w for w in xx if re.search('(Year|Birth|irth|YoB|YOB:|DOB:|DOB)$', w)]:
        yearline = wordlist
        break
    else:
        text1.append(wordlist)
try:
    text2 = text.split(yearline,1)[1]
except:
    pass

try:
    yearline = re.split('Birth : |Birth:|Birth|Birth |irth|Year|YoB|YOB:|DOB:|DOB : | DOB :|DOB', yearline)[1:]
    print(yearline[-1])
    dob = yearline[-1].strip()
    # yearline = ''.join(str(e) for e in yearline)
    # if yearline:
    #     dob = dparser.parse(yearline, fuzzy=True)
except:
    pass


# Searching for Gender
try:
	for wordlist in lines.split('\n'):
		xx = wordlist.split( )
		if ([w for w in xx if re.search('(Female|Male|emale|male|ale|FEMALE|MALE|EMALE)$', w)]):
			genline = wordlist
			break

	if 'Female' in genline:
	    gender = "Female"
	if 'Male' in genline:
	    gender = "Male"

	text2 = texttemp.split(genline,1)[1]

except:
	pass

#-----------Read Database
with open('namedb1.csv', 'rb') as f:
	reader = csv.reader(f)
	newlist = list(reader)    
newlist = sum(newlist, [])


# Searching for Name and finding closest name in database
try:
	text1 = filter(None, text1)
	for x in text1:
		for y in x.split( ):
			if(difflib.get_close_matches(y.upper(), newlist)):
				nameline.append(x)
				break
	name = ''.join(str(e) for e in nameline)
except:
	pass


# Searching for UID

# print(newlist)

try:
	newlist = []
	for xx in text2.split('\n'):
		newlist.append(xx)
	newlist = filter(lambda x: len(x)>5, newlist)
	ma = 0
	uid = ''.join(str(e) for e in newlist)
	for no in newlist:
		if ma<sum(c.isdigit() for c in no):
			ma = sum(c.isdigit() for c in no)
			uid = int(filter(str.isdigit, no))
except:
	pass



print(name, gender, dob, uid)

# # Making tuples of data
data = {}
data['Name'] = name
data['Gender'] = gender
data['DOB'] = dob
data['Uid'] = uid
# '''
# Writing data into JSON
with open('../result/'+ os.path.basename(sys.argv[1]).split('.')[0] +'.json', 'w') as fp:
    json.dump(data, fp)
# '''
#
# # Removing dummy files
# os.remove('temp.jpg')
#
# '''
# # Reading data back JSON
# with open('../result/'+ os.path.basename(sys.argv[1]).split('.')[0] +'.json', 'r') as f:
#      ndata = json.load(f)
# #'''
# print("+++++++++++++++++++++++++++++++")
# print(data['Name'])
# print("-------------------------------")
# print(data['Gender'])
# print("-------------------------------")
# print(data['Birth year'])
# print("-------------------------------")
# print(data['Uid'])
# print("-------------------------------")
# #'''
