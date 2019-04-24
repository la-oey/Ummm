#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on March 28

@author: loey
"""

import time
import sys
import csv
import string
import re
csv.field_size_limit(sys.maxsize)
filenames = dict()
escapes = ''.join([chr(char) for char in range(1, 32)])

def main():
	start_time = time.time()
	read_file = 'split/'+sys.argv[1]+'_allFiles'
	with open(read_file+'.csv', 'r') as csv_file_r:
		csv_file_w = open(read_file+'_awdPrePro.csv', 'w')
		fieldnames = ['filename', 'author', 'subreddit', 'title', 'text', 'cleanedText', 'sentLength', 'timestamp']
		writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
		writer.writeheader()
		reader = csv.DictReader(csv_file_r)
		index = 0
		for r in reader:
			if r['filename'] not in filenames:
				filenames[r['filename']] = [r['filename']]
				print(r['filename'])
			newText = re.sub('([.,!?()\'\"])', r' \1 ', r['text'])
			newText = re.sub('\\s{2,}', ' ', newText)
			sentLength = len(newText.split())
			#newText = r['text'].translate(str.maketrans('','',escapes))
			cleanedText = ' '.join([str(c) if c != ord('\n') else '\n' for c in r['text']])
			writer.writerow({'filename': r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'text':newText, 'cleanedText':cleanedText, 'sentLength':sentLength, 'timestamp': r['timestamp']})
		csv_file_w.close()
		csv_file_r.close()
	print("awd-lstm-lm_prepro.py Run Time: " + str(time.time()-start_time) + " seconds")

main()