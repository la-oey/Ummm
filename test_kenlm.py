#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:03:27 2018

@author: loey
"""

import time
import kenlm
import sys
import csv
csv.field_size_limit(sys.maxsize)
from nltk.tokenize import RegexpTokenizer
filenames = dict()
start_time = time.time()
model = kenlm.LanguageModel('../kenlm/build/reddit.binary')
#sentence = 'this is a sentence .'
#print(model.score(sentence))
model_train_end_time = time.time()
model_train_time = model_train_end_time - start_time

def main():
	with open('postExtract/sample_'+sys.argv[1]+'_allFiles.csv', 'r') as csv_file_r:
		csv_file_w = open('umm_kenlm_output_'+sys.argv[1]+'.csv', 'w')
		reader = csv.DictReader(csv_file_r)
		fieldnames = ['filename', 'author', 'subreddit', 'title', 'lexicalType', 'lexicalItem', 'lexicalLength', 'lexicalIndex', 'text', 'sentLength', 'timestamp', 'sentScore', 'fullScores']
		writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
		writer.writeheader()

		for r in reader:
			if r['filename'] not in filenames:
				filenames[r['filename']] = [r['filename']]
				print(r['filename'])

			score = model.score(r['text'])
			scoreArr = []
			for j, (prob, length, oov) in enumerate(model.full_scores(r['text'])):
				scoreArr.append(prob)

			writer.writerow({'filename':r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'lexicalType':r['lexicalType'], 'lexicalItem':r['lexicalItem'], 'lexicalLength':r['lexicalLength'], 'lexicalIndex':r['lexicalIndex'], 'text':r['text'], 'sentLength':r['sentLength'], 'timestamp':r['timestamp'], 'sentScore':score, 'fullScores':scoreArr})
		csv_file_w.close()
		csv_file_r.close()
	print("Model Run Time: " + str(model_train_time) + " seconds")
	print("test_kenlm.py Run Time: " + str(time.time()-model_train_end_time) + " seconds")

main()
