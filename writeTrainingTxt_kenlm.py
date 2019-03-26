#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 18:26:56 2018

@author: loey
"""

import time
import sys
import csv
import re
csv.field_size_limit(sys.maxsize)
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
filenames = dict()

def main():
    start_time = time.time()
    with open('split/training_allFiles.csv', 'r') as csv_file_r:
        training_file = open('train_kenlm.txt', 'w')
        reader = csv.DictReader(csv_file_r)
        
        for r in reader:
            if r['filename'] not in filenames:
                filenames[r['filename']] = [r['filename']]
                print(r['filename'])

            newSentAsString = ""
            cleaned = tokenizer.tokenize(r['text'].lower())
            if any(re.match("^umm+$", x) for x in cleaned):
                newSent = []
                for w in cleaned: 
                    if not re.match("^umm+$", w):
                        newSent.append(w)
                newSentAsString = " ".join(newSent)
            else:
            	newSentAsString = " ".join(cleaned)
            
            training_file.write(newSentAsString + "\n")
        training_file.close()
        csv_file_r.close()
    print("writeTrainingTxt_kenlm.py Run Time: " + str(time.time()-start_time) + " seconds")

main()