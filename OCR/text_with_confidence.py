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
from utilities import processor
from operator import itemgetter
from collections import defaultdict
from PIL import Image, ImageEnhance, ImageFilter
import uuid


def do(image, rgb, conf):
	try:
		word_list = extract_words(image, rgb, conf)
	except:
		print("Exception getting word list", rgb, conf)
	try:
		lines = get_lines(word_list)
		return lines
	except:
		print("Exception getting lines", rgb, conf)


# Returns sorted list of extracted words
def extract_words(image, rgb, confidence):
	# Variable Constants
	unique_id = str(uuid.uuid4())
	processed_image = '/tmp/processed_image_' + unique_id + '.jpg'
	processed_tsv = '/tmp/processed_tsv_' + unique_id
	# Preprocess image
	processor.preprocess(image, rgb, processed_image)
	# Get word list
	parsed_word_list = get_word_list(processed_image, processed_tsv, confidence)
	os.remove(processed_tsv + '.tsv')
	os.remove(processed_image)

	# Need List of objects sorted in order of block, line, word
	parsed_word_list = sorted(parsed_word_list, key=itemgetter('block_num', 'par_num', 'line_num', 'word_num'))
	return parsed_word_list


# Call tesseract for image and get word list from resulting tsv
def get_word_list(processed_image, processed_tsv, confidence):
	# processed_text = pytesseract.image_to_string(Image.open('processed.jpg'))
	subprocess.call("tesseract " + processed_image + " " + processed_tsv + " --oem 1 -l eng tsv", shell=True)
	parsed_word_list = processor.parse_tsv_with_nonzero_confidence(processed_tsv+'.tsv', confidence)
	return parsed_word_list


def get_lines(word_list):
	mylist = {}
	if len(word_list) == 0:
		return {}

	mylist[0] = [word_list[0]["text"]]
	j = 0
	for i in range(1, len(word_list)):
		if i == len(word_list):
			break
		entry = word_list[i]
		previous_entry = word_list[i-1]
		text = filter(lambda x: ord(x) > 31 and ord(x) < 128, entry["text"])
		if len(text.strip()) == 0:
			continue
		if entry["block_num"] == previous_entry["block_num"] and entry["par_num"] == previous_entry["par_num"] and entry["line_num"] == previous_entry["line_num"]:
			mylist[j].append(text)
		else:
			j = j + 1
			mylist[j] = [text]
	return mylist


# TRY WITH 2 OR 3 DIFFERENT LIGHTING CONDITIONS RGB (80, 100, 120)
# get(sys.argv[1], 70, 30)
