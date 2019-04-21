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

import imageio
import numpy as np


# Run text_with_confidence X times with rgb = rgb + y and Y times with confidence c = c + d

def run(file):
	mean = np.mean(imageio.imread(file, as_gray=True))
	# print("Mean rgb", mean) # this wont work because words are black
	
	# Have to adjust rgb, max_rgb, inc as needed
	rgb = 70
	max_rgb = mean/1.5
	inc = 10
	image_list = []
	while rgb <= max_rgb:
		image_list.append( { "image": file, "rgb": rgb, "conf": 30} )
		rgb = rgb + inc
	print("Running for " + str(len(image_list)) + " different versions of image")
	no_of_proc = len(image_list) #5
	lines = fast.process(image_list, no_of_proc)
	return lines


def get_info(lines_list):
	aadhar_no = ''
	name = ''
	sex = ''
	date_of_birth = ''
	found_dob = False
	sex_line_index = len(lines_list)
	for index in lines_list:
		line = lines_list[index]
		
		# Aadhar Number
		if len(aadhar_no) != 12:
			aadhar_no = ''
			for word in line:
				word = filter(lambda x: ord(x) == 32 or ord(x) == 35 or (ord(x) >= 48 and ord(x) <= 90) or (ord(x) >= 97 and ord(x) <= 122), word)
				if word.isdigit() and aadhar_no != word: # handle repeating pincode
					aadhar_no += word
		
		# Date of Birth
		joined_line = ''.join(str(e) for e in line)
		found_dob_index = re.search('Birth : |Birth:|Birth|Birth |irth|Year : | Year:|YoB|YOB : |YOB:|DOB:|DOB : | DOB :|DOB', joined_line);
		if found_dob_index >= 0:
			date_of_birth = joined_line[found_dob_index.end():]
			sex_line_index = index + 1
		
		# Sex
		if index == sex_line_index:
			if ([w for w in line if re.search('(Female|Male|emale|male|ale|FEMALE|MALE|EMALE)$', w)]):
				joined_line = ''.join(str(e) for e in line)
			if 'female' in joined_line.lower():
				sex = 'Female'
			if 'male' in joined_line.lower():
				sex = 'Male'
				
	return aadhar_no, date_of_birth, sex


file = sys.argv[1]
all_lines = run(file)
print('Getting aadhar...')
extracted_data_list = []
extracted_aadhar_list = []
extracted_dob_list = []
extracted_sex_list = []
for lines in all_lines:
	aadhar_no, date_of_birth, sex = get_info(lines)
	# print(aadhar_no, date_of_birth, sex)
	extracted_aadhar_list.append(aadhar_no)
	extracted_dob_list.append(date_of_birth)
	extracted_sex_list.append(sex)
	extracted_data_list.append( { "aadhar_no": aadhar_no, "dob": date_of_birth, "sex": sex } )

final_data = {
	"Aadhar No": max(set(extracted_aadhar_list), key = extracted_aadhar_list.count),
	"DOB": max(set(extracted_dob_list), key = extracted_dob_list.count),
	"Sex": max(set(extracted_sex_list), key = extracted_sex_list.count)
}
print(final_data)

# Writing data into JSON
with open('result/aadhar.json', 'a') as fp:
	# json.dump(data, fp)
	fp.write(str(final_data) + "\n")


"""
# Read Name Database
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
