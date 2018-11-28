#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 12:29:18 2018

@author: loey
"""

import time
import sys
import csv
import json
import json.decoder
import os
import nltk
from os import listdir
from os.path import isfile, join

def convertToTrain(writer, fileName, file):
    reddit_info = []
    for i in range(0,len(file)):
        try:
            asDict = json.loads(file[i])
            
            if 'author' in asDict:
                author = asDict['author']
            else:
                author = 'NA'
            
            if 'subreddit' in asDict:
                subreddit = asDict['subreddit']
            else:
                subreddit = 'NA'
            
            if 'title' in asDict:
                title = asDict['title']
            else:
                title = 'NA'
            
            if 'created_utc' in asDict:
                timestamp = asDict['created_utc']
            else:
                timestamp = 'NA'

            if asDict['selftext'] != "":
                reddit_sent = nltk.sent_tokenize(asDict['selftext'])
                for s in range(0, len(reddit_sent)):
                    writer.writerow({'filename': fileName, 'author':author, 'subreddit':subreddit, 'title':title, 'text':reddit_sent[s], 'timestamp': timestamp})
            else:
                writer.writerow({'filename': fileName, 'author':author, 'subreddit':subreddit, 'title':title, 'text':'NA', 'timestamp': timestamp})
        except ValueError as e: #catches syntax error in text file
            pass
            
    return(reddit_info)


def main():
    start_time = time.time()
    mypath = sys.argv[1] + "/" #set path to folder containing files
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    with open('rawtxt/raw_'+sys.argv[1]+'.csv', 'w') as csv_file:
        fieldnames = ['filename', 'author', 'subreddit', 'title', 'text', 'timestamp']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for f in files:
            print(f)
            reddit = open(mypath+f, 'r')
            reddit_fulltxt = reddit.readlines()
            reddit_editedtxt = convertToTrain(writer, f, reddit_fulltxt)
            reddit.close()
        csv_file.close()
    print("Run Time: " + str(time.time()-start_time) + " seconds")
main()

