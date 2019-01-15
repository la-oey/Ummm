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

filenames = dict()

def main():
    start_time = time.time()
    with open('split/'+sys.argv[1]+'_allFiles.csv', 'r') as csv_file_r:
    	if sys.argv[1] == "training":
    		name = "train"
    	elif sys.argv[1] == "training_valid":
    		name = "valid"
    	else:
    		name = "test"
        training_file = open('redditTrain/'+name+'.txt', 'w')
        reader = csv.DictReader(csv_file_r)
        
        for r in reader:
            if r['filename'] not in filenames:
                filenames[r['filename']] = [r['filename']]
                print(r['filename'])

            newSentAsString = ""
            if r['sentLength'] != None and any(re.match("^umm+$", x) for x in r['text'].split()):
                newSent = []
                for w in r['text'].split(): 
                    if not re.match("^umm+$", w):
                        newSent.append(w)
                newSentAsString = " ".join(newSent)
            
            training_file.write(newSentAsString + "\n")
        training_file.close()
        csv_file_r.close()
    print("writeTrainingTxt.py Run Time: " + str(time.time()-start_time) + " seconds")

main()