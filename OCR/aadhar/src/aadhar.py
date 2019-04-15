#!/usr/bin/env python
import os.path
import json
import sys
import pytesseract
import re
import difflib
import csv
import nltk
import subprocess
from PIL import Image, ImageEnhance, ImageFilter

frontpath = sys.argv[1]
# path = "/Users/mohit/Downloads/aadhar.jpg"

img = Image.open(frontpath)
img = img.convert('RGBA')
# img = img.filter(ImageFilter.SHARPEN)
pix = img.load()

# Cropping
for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
            pix[x, y] = (0, 0, 0, 255)
        else:
            pix[x, y] = (255, 255, 255, 255)

img.save('processed.jpg')

# Call tesseract for orig image and sharpened image

# original_text = pytesseract.image_to_string(img)
# processed_text = pytesseract.image_to_string(Image.open('processed.jpg'))

subprocess.call("tesseract "+frontpath+" original_text ", shell=True)
# subprocess.call("tesseract processed.jpg processed_text ", shell=True)
subprocess.call("tesseract processed.jpg processed_text  -l eng hin tsv", shell=True)
# subprocess.call("tesseract processed.jpg processed_text_hin  -l hin csv", shell=True)
#
original_text_file = open('original_text.txt', 'r')
original_text = original_text_file.read()
processed_text_file = open('processed_text.txt', 'r')
processed_text = processed_text_file.read()

original_text = filter(lambda x: ord(x) < 128, original_text)
processed_text = filter(lambda x: ord(x) < 128, processed_text)

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

	img = Image.open(backpath)
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

	img.save('processed_back.jpg')

	subprocess.call("tesseract "+backpath+" original_text_back ", shell=True)
	# subprocess.call("tesseract processed_back.jpg processed_text_back ", shell=True)
	subprocess.call("tesseract processed_back.jpg processed_text_back  -l eng hin tsv ", shell=True)
	# subprocess.call("tesseract processed_back.jpg processed_text_back_hin  -l hin csv ", shell=True)


	original_text_file = open('original_text_back.txt', 'r')
	original_text = original_text_file.read()
	processed_text_file = open('processed_text_back.txt', 'r')
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



