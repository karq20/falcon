#!/usr/bin/env python
import os.path
import json
import sys
import pytesseract
import re
import difflib
import csv
import nltk
import time
import subprocess
import text_with_confidence
from operator import itemgetter
from PIL import Image, ImageEnhance, ImageFilter
import fast


# Run text_with_confidence X times with rgb = rgb + y and Y times with confidence c = c + d

def run():
	# 9 sec with multithreading
	image_list = ['./test/data/aadhar/aadhar.jpg', './test/data/aadhar/aadharback.jpg', './test/data/aadhar/soham.jpeg', './test/data/aadhar/sohamback2.jpeg']
	no_of_proc = 4
	lines = fast.process(image_list, 90, 40, no_of_proc)
	return lines

print(run())


"""
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
lines = processed_text

for wordlist in lines.split('\n'):
    xx = wordlist.split( )
    if [w for w in xx if re.search('(Year|Birth|irth|YoB|YOB:|DOB:|DOB)$', w)]:
        yearline = wordlist
        break
    else:
        text1.append(wordlist)
try:
    text2 = processed_text.split(yearline,1)[1]
except:
    pass

try:
    yearline = re.split('Birth : |Birth:|Birth|Birth |irth|Year|YoB|YOB:|DOB:|DOB : | DOB :|DOB', yearline)[1:]
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

	text2 = processed_text.split(genline,1)[1]

except:
	pass

# Read Database
with open('namedb.csv', 'rb') as f:
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


# Searching for Aadhar No

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


# Removing dummy files
# os.remove('processed.jpg')
# os.remove('original_text.txt')
# os.remove('processed_text.txt')


# Making tuples of data
data = {}
data['Name'] = name
data['Gender'] = gender
data['DOB'] = dob
data['Aadhar'] = uid


############################## BACK ##################################
pincode = None

backpath = ''
if len(sys.argv) > 2:
	backpath = sys.argv[2]
	backpath_processed = "processed_back.jpg"

	preprocess(backpath, 102, 102, 102, backpath_processed)

	subprocess.call("tesseract " + backpath + " text_back -l eng hin tsv ", shell=True)
	subprocess.call("tesseract " + backpath_processed + " proctext_back -l eng hin tsv ", shell=True)

	original_text_file = open('text_back.txt', 'r')
	original_text = original_text_file.read()
	processed_text_file = open('proctext_back.txt', 'r')
	processed_text = processed_text_file.read()

	original_text = filter(lambda x: ord(x) < 128, original_text)
	processed_text = filter(lambda x: ord(x) < 128, processed_text)

	lines = processed_text

	found = False
	count = 0
	for wordlist in lines.split('\n'):
		count = count+1
		if count < 3:
			pass
		for word in wordlist.split():
			if len(word) == 6 and word.isdigit():
				pincode = word
				found = True
				break
		if found:
			break

	# Removing dummy files
	# os.remove('processed_back.jpg')
	# os.remove('original_text_back.txt')
	# os.remove('processed_text_back.txt')

data['Pincode'] = pincode

print('------------------------------------- PARSED AADHAR OUTPUT -------------------------------------------------')
print(data)
print('------------------------------------------------------------------------------------------------------------')


# Writing data into JSON
with open('../result/' + os.path.basename(sys.argv[1]).split('.')[0] + '.json', 'w') as fp:
	json.dump(data, fp)


"""
