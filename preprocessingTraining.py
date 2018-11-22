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
from html.parser import HTMLParser
import langid

tokenizer = RegexpTokenizer(r'\w+')
pattern_http = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
pattern_www = re.compile('www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
pattern_ = re.compile('_*')
filenames = dict()
botdict = dict()

def main():
    start_time = time.time()
    with open('rawtxt/raw_'+sys.argv[1]+'.csv', 'r') as csv_file_r:
        botfile = open('redditbots.txt', 'r')
        for b in botfile.read().splitlines():
            botdict[b] = [b]
        botfile.close()

        csv_file_w = open('preprocessed/processed_'+sys.argv[1]+'.csv', 'w')
        reader = csv.DictReader(csv_file_r)
        fieldnames = ['filename', 'author', 'subreddit', 'title', 'text', 'sentLength', 'timestamp']
        writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
        writer.writeheader()
        for r in reader:
            if r['filename'] not in filenames:
                filenames[r['filename']] = [r['filename']]
                print(r['filename'])
            text = r['text']
            author = r['author']
            if (text not in ["NA", "[deleted]", "[removed]"]) and (author not in ["[deleted]", "autotldr"]) and (author not in botdict) and (re.match("bot$",author) == None) and (langid.classify(text)[0] == "en"): #removes deleted comments
                text = pattern_http.sub('', text)
                text = pattern_www.sub('', text)
                text = pattern_.sub('', text)
                text = HTMLParser().unescape(text)
                
                cleaned_arr = tokenizer.tokenize(text.lower())
                cleaned = ' '.join(cleaned_arr)
                    
                writer.writerow({'filename': r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'text':cleaned, 'sentLength':len(cleaned_arr), 'timestamp': r['timestamp']})
        csv_file_w.close()
        csv_file_r.close()
    print("Run Time: " + str(time.time()-start_time) + " seconds")

main()
    