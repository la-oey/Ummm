#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:03:27 2018

@author: loey
"""

import time
import sys
import csv
import random
csv.field_size_limit(sys.maxsize)

author_training = dict()
author_validation = dict()
author_testing = dict()
filenames = dict()

# proportion of data in each set
p_train = 0.70
p_validate = 0.10
p_test = 0.20

def main():
    start_time = time.time()
    with open('preprocessed/processed_'+sys.argv[1]+'.csv', 'r') as csv_file_r:
        training_file = open('split/training_'+sys.argv[1]+'.csv', 'w')
        validation_file = open('split/validation_'+sys.argv[1]+'.csv', 'w')
        testing_file = open('split/testing_'+sys.argv[1]+'.csv', 'w')
        
        reader = csv.DictReader(csv_file_r)
        fieldnames = ['filename', 'author', 'subreddit', 'title', 'text', 'sentLength', 'timestamp']
        training = csv.DictWriter(training_file, fieldnames=fieldnames)
        training.writeheader()
        validation = csv.DictWriter(validation_file, fieldnames=fieldnames)
        validation.writeheader()
        testing = csv.DictWriter(testing_file, fieldnames=fieldnames)
        testing.writeheader()
        
        for r in reader:
            if r['filename'] not in filenames:
                filenames[r['filename']] = [r['filename']]
                print(r['filename'])
            
            rowinfo = {'filename': r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'text':r['text'], 'sentLength':r['sentLength'], 'timestamp': r['timestamp']}
            if r['author'] in author_training:
                training.writerow(rowinfo)
            elif r['author'] in author_validation:
                validation.writerow(rowinfo)
            elif r['author'] in author_testing:
                testing.writerow(rowinfo)
            else:
                rand = random.random()
                if rand < p_train:
                    author_training[r['author']] = [r['author']]
                    training.writerow(rowinfo)
                elif rand < (p_train + p_validate):
                    author_validation[r['author']] = [r['author']]
                    validation.writerow(rowinfo)
                else:
                    author_testing[r['author']] = [r['author']]
                    testing.writerow(rowinfo)
        csv_file_r.close()
        training_file.close()
        validation_file.close()
        testing_file.close()
    print("Run Time: " + str(time.time()-start_time) + " seconds")
                    
main()          
        