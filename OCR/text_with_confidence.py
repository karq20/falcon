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


def get(image, rgb, confidence_threshold):

	# Variable Constants
	processed_image = '/tmp/frontpath_processed.jpg'
	processed_tsv = '/tmp/proctext'

	processor.preprocess(image, rgb, processed_image)

	# Call tesseract for orig image and sharpened image
	# original_text = pytesseract.image_to_string(img)
	# processed_text = pytesseract.image_to_string(Image.open('processed.jpg'))
	# subprocess.call("tesseract " + frontpath + " text -l eng tsv", shell=True)
	subprocess.call("tesseract " + processed_image + " " + processed_tsv + " -l eng tsv", shell=True)
	# original_text_file = open('text.tsv', 'r')
	# original_text = original_text_file.read()
	# processed_text_file = open('proctext.tsv', 'r')
	# processed_text = processed_text_file.read()
	# original_text = filter(lambda x: ord(x) < 128, original_text)
	# processed_text = filter(lambda x: ord(x) < 128, processed_text)

	parsed_word_list = processor.parse_tsv_with_nonzero_confidence(processed_tsv+'.tsv', confidence_threshold)

	""" Need List of objects sorted in order of block, line, word """

	block_map = {}

	parsed_word_list = sorted(parsed_word_list, key=itemgetter('block_num', 'par_num', 'line_num', 'word_num'))

	mylist = {}
	mylist[0] = [parsed_word_list[0]["text"]]
	j = 0
	for i in range(1, len(parsed_word_list)):
		if i == len(parsed_word_list):
			break

		entry = parsed_word_list[i]
		previous_entry = parsed_word_list[i-1]
		text = filter(lambda x: ord(x) > 31 and ord(x) < 128, entry["text"])
		conf = entry["conf"]
		block = entry["block_num"]
		par = entry["par_num"]
		line = entry["line_num"]
		word = entry["word_num"]
		if len(text.strip()) == 0:
			continue

		if block == previous_entry["block_num"]	and par == previous_entry["par_num"] and line == previous_entry["line_num"]:
			mylist[j].append(text)
		else:
			j = j + 1
			mylist[j] = [text]

	os.remove(processed_image)
	os.remove(processed_tsv+'.tsv')

	return mylist

# TRY WITH 2 OR 3 DIFFERENT LIGHTING CONDITIONS (80, 100, 120)
# get(sys.argv[1], 70, 30)
# get(sys.argv[1], 80, 30)
# get(sys.argv[1], 90, 30)
# get(sys.argv[1], 100, 30)
# get(sys.argv[1], 110, 30)
get(sys.argv[1], 120, 30)
