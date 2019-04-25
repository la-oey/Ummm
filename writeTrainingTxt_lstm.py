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
    for i in ["train", "valid", "test"]:
    	with open('split/training_'+i+'_allFiles.csv', 'r') as csv_file_r:
	        training_file = open('redditTrain/'+i+'.txt', 'w')
	        reader = csv.DictReader(csv_file_r)
	        for r in reader:
	            if r['filename'] not in filenames:
	                filenames[r['filename']] = [r['filename']]
	                print(r['filename'])

	            newSentAsString = ' '.join([str(c) if c != ord('\n') else '\n' for c in r['text']])
	            training_file.write(newSentAsString + "\n")
	        training_file.close()
	        csv_file_r.close()
    
    print("writeTrainingTxt_lstm.py Run Time: " + str(time.time()-start_time) + " seconds")

main()