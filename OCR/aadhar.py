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
import processor
from operator import itemgetter
from PIL import Image, ImageEnhance, ImageFilter


def preprocess(imgpath, tR, tG, tB, processed_img):
	img = Image.open(imgpath)
	img = img.convert('RGBA')
	# img = img.filter(ImageFilter.SHARPEN)
	pix = img.load()

	# Convert to black and white
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			if pix[x, y][0] < tR or pix[x, y][1] < tG or pix[x, y][2] < tB:
				pix[x, y] = (0, 0, 0, 255)
			else:
				pix[x, y] = (255, 255, 255, 255)

	img.save(processed_img)


frontpath = sys.argv[1]
frontpath_processed = 'frontpath_processed.jpg'
rgb = 90
preprocess(frontpath, rgb, rgb, rgb, frontpath_processed)

# Call tesseract for orig image and sharpened image
# original_text = pytesseract.image_to_string(img)
# processed_text = pytesseract.image_to_string(Image.open('processed.jpg'))

# subprocess.call("tesseract " + frontpath + " text -l eng tsv", shell=True)
subprocess.call("tesseract " + frontpath_processed + " proctext -l eng tsv", shell=True)

# original_text_file = open('text.tsv', 'r')
# original_text = original_text_file.read()
processed_text_file = open('proctext.tsv', 'r')
processed_text = processed_text_file.read()

# original_text = filter(lambda x: ord(x) < 128, original_text)
processed_text = filter(lambda x: ord(x) < 128, processed_text)

print("------ Processed Text -----")

parsed_word_list = processor.parse_tsv_with_confidence('proctext.tsv', 60)

"""
Need List of objects sorted in order of block, line, word
"""

block_map = {}

parsed_word_list = sorted(parsed_word_list, key=itemgetter('block_num', 'line_num', 'word_num'))


# print(parsed_word_list)
for entry in parsed_word_list:
	text = entry["text"]
	conf = entry["conf"]
	block = entry["block_num"]
	par = entry["par_num"]
	line = entry["line_num"]
	word = entry["word_num"]
	print(text, conf, block, par, line, word)





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
