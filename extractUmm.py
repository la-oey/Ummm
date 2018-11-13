#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:24:40 2018

@author: Lauren_Oey
"""

import re
import sys
import csv
csv.field_size_limit(sys.maxsize)
import nltk
from nltk import word_tokenize

authors = dict()


def main():
    totalWords = 0
    ummWords = 0
    with open('preExtract/processed_'+sys.argv[1]+'.csv', 'r') as csv_file_r:
        csv_file_w = open('postExtract/sample_'+sys.argv[1]+'.csv', 'w')
        reader = csv.DictReader(csv_file_r)
        fieldnames = ['filename', 'author', 'subreddit', 'title', 'lexicalType', 'lexicalItem', 'lexicalLength', 'text', 'sentLength', 'timestamp']
        writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
        writer.writeheader()
        meta_file = open('postExtract/metadata_'+sys.argv[1]+'.txt', 'w')
        
        for r in reader:
            if r['sentLength'] != None:
                totalWords = totalWords + int(r['sentLength'])
                # checks for word match to umm and checks that sentence contains more than one word
                if any(re.match("^umm+$", x) for x in r['text'].split()) and int(r['sentLength']) > 1:
                    # checks if comment author exists as an entry in dictionary of authors
                    # if author does not exist, create an entry & sets value to an array containing the length of the sentence
                    if r['author'] not in authors:
                        authors[r['author']] = [r['sentLength']]
                    # if author does exists, but length of sentence is not contained within the array of sentence lengths, adds the length to the array
                    elif r['sentLength'] not in authors[r['author']]:
                        authors[r['author']].append(r['sentLength'])
                                
                    # loops through each word in the sentence and finds the word match
                    # used for retrieving the word and the length of the word
                    # records a row in the csv for each word match
                    for w in r['text'].split():  
                        if re.match("^umm+$", w):
                            writer.writerow({'filename':r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'lexicalType':'umm', 'lexicalItem':w, 'lexicalLength':len(w), 'text':r['text'], 'sentLength':r['sentLength'], 'timestamp':r['timestamp']})
                            ummWords = ummWords + 1

                # collects controls
                # checks among non-umm containing sentences if author entry exists and sentence length is contained within the array
                elif r['author'] in authors and r['sentLength'] in authors[r['author']]:
                    writer.writerow({'filename':r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'lexicalType':'control', 'lexicalItem':'NA', 'lexicalLength':'NA', 'text':r['text'], 'sentLength':r['sentLength'], 'timestamp':r['timestamp']})

        meta_file.write('Total Words in File: ' + str(totalWords) + "\nUmm Words in Files: " + str(ummWords))
        meta_file.close()
        csv_file_w.close()

main()
