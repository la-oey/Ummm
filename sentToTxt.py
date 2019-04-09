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
csv.field_size_limit(sys.maxsize)
filenames = dict()
escapes = ''.join([chr(char) for char in range(1, 32)])

def main():
	start_time = time.time()
	read_file = 'split/'+sys.argv[1]+'_allFiles'
	with open(read_file+'.csv', 'r') as csv_file_r:
		csv_file_w = open(read_file+'_txt.csv', 'w')
		fieldnames = ['index', 'cleanedText']
		writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
		writer.writeheader()
		csv_file_w2 = open(read_file+'_full.csv', 'w')
		fieldnames2 = ['index', 'filename', 'author', 'subreddit', 'title', 'text', 'sentLength', 'timestamp']
		writer2 = csv.DictWriter(csv_file_w2, fieldnames=fieldnames2)
		writer2.writeheader()
		reader = csv.DictReader(csv_file_r)
		index = 0
		for r in reader:
			if r['filename'] not in filenames:
				filenames[r['filename']] = [r['filename']]
				print(r['filename'])
			newText = r['text'].translate(str.maketrans('','',escapes))
			writer.writerow({'index':index, 'cleanedText':newText})
			writer2.writerow({'index':index, 'filename': r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'text':newText, 'sentLength':r['sentLength'], 'timestamp': r['timestamp']})
			index = index + 1
		csv_file_w.close()
		csv_file_w2.close()
		csv_file_r.close()
	print("sentToTxt.py Run Time: " + str(time.time()-start_time) + " seconds")

main()