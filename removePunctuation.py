#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 14:43:40 2018

@author: loey
"""

import time
import re
import sys
import csv
csv.field_size_limit(sys.maxsize)
from nltk.tokenize import RegexpTokenizer

filenames = dict()
tokenizer = RegexpTokenizer(r'\w+')

def main():
    start_time = time.time()
    with open('preprocessed/processed_allFiles.csv', 'r') as csv_file_r:
        csv_file_w = open('preprocessed/noPunct_allFiles.csv', 'w')
        reader = csv.DictReader(csv_file_r)
        fieldnames = ['filename', 'author', 'subreddit', 'title', 'text', 'sentLength', 'timestamp']
        writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
        writer.writeheader()
        for r in reader:
            if r['filename'] not in filenames:
                filenames[r['filename']] = [r['filename']]
                print(r['filename'])
            cleaned_arr = tokenizer.tokenize(r['text'].lower())
            cleaned = ' '.join(cleaned_arr)
                    
            writer.writerow({'filename': r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'text':cleaned, 'sentLength':len(cleaned_arr), 'timestamp': r['timestamp']})
        csv_file_w.close()
        csv_file_r.close()
    print("Run Time: " + str(time.time()-start_time) + " seconds")

main()
    