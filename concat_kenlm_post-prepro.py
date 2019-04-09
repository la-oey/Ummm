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
cleaned = dict()

def main():
	start_time = time.time()
	read_file = 'split/'+sys.argv[1]+'_allFiles'
	with open(read_file+'_full.csv', 'r') as csv_file_r_full:
		csv_file_r_txt = open(read_file+'_cleaned.csv', 'r')
		reader = csv.DictReader(csv_file_r_full)
		reader_txt = csv.DictReader(csv_file_r_txt)
		csv_file_w = open(read_file+'_concat.csv', 'w')
		fieldnames = ['index', 'filename', 'author', 'subreddit', 'title', 'text', 'sentLength', 'timestamp', 'cleanedText']
		writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
		writer.writeheader()

		index = 0
		for rt in reader_txt:
			if rt[' cleanedText '] is not None:
				if re.match("^\\d+\\s*$", rt['index ']) and rt['index '].strip() not in cleaned:
					cleaned[rt['index '].strip()] = [rt[' cleanedText ']]
					if None in rt:
						for s in rt[None]:
							cleaned[rt['index '].strip()].append(s)
					index = rt['index '].strip()
				else:
					cleaned[index].append(rt['index '])
					cleaned[index].append(rt[' cleanedText '])
					if None in rt:
						for s in rt[None]:
							cleaned[index].append(s)
			else:
				if re.match("^\\d+\\s*$", rt['index ']) and rt['index '].strip() not in cleaned:
					cleaned[rt['index '].strip()] = []
					index = rt['index '].strip()
				else:
					cleaned[index].append(rt['index '])

		for r in reader:
			if r['filename'] not in filenames:
				filenames[r['filename']] = [r['filename']]
				print(r['filename'])
			if r['index'] in cleaned:
				cleanedText = "".join(cleaned[r['index']])
				writer.writerow({'index':r['index'], 'filename': r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'text':r['text'], 'sentLength':r['sentLength'], 'timestamp': r['timestamp'], 'cleanedText':cleanedText})
			else:
				writer.writerow({'index':r['index'], 'filename': r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'text':r['text'], 'sentLength':r['sentLength'], 'timestamp': r['timestamp'], 'cleanedText':'NA'})
		csv_file_r_full.close()
		csv_file_r_txt.close()
		csv_file_w.close()
	print("concat_kenlm_post-prepro.py Run Time: " + str(time.time()-start_time) + " seconds")
main()

