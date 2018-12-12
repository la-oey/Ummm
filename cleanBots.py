#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 18:26:56 2018

@author: loey
"""

# cleans bots and splits authors contributing > 1/1000 to the data

import time
import sys
import csv
import re
csv.field_size_limit(sys.maxsize)

filenames = dict()
authors = dict()

def main():
    start_time = time.time()

    with open('preprocessed/processed_allFiles.csv', 'r') as csv_file_r:
        csv_file_w = open('cleanAuthor/processed_allFiles.csv', 'w')
        reader = csv.DictReader(csv_file_r)
        fieldnames = ['filename', 'author', 'subreddit', 'title', 'text', 'sentLength', 'timestamp']
        writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
        writer.writeheader()
        for r in reader:
            if r['filename'] not in filenames:
                filenames[r['filename']] = [r['filename']]
                print(r['filename'])
            
            rowinfo = {'filename': r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'text':r['text'], 'sentLength':r['sentLength'], 'timestamp': r['timestamp']}
            if not re.match("^.+(bot)$", r['author'], re.IGNORECASE) and (r['author'] not in ["peterboykin","censorship_notifier","AutoModerator","subredditreports","scamcop"]):
                writer.writerow(rowinfo)

        csv_file_r.close()
        csv_file_w.close()
        
    print("cleanBots.py Run Time: " + str(time.time()-start_time) + " seconds")

main()