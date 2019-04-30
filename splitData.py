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
author_training_tr = dict()
author_training_va = dict()
author_training_te = dict()
author_validation = dict()
author_testing = dict()
filenames = dict()

# proportion of data in each set
p_train = 0.3
p_train_tr = 0.09
p_train_va = 0.005
p_train_te = 0.005
p_validate = 0.35
p_test = 0.35

def main():
    start_time = time.time()
    with open('preprocessed/noPunct_allFiles.csv', 'r') as csv_file_r:
        training_file = open('split/training_allFiles.csv', 'w')
        training_train_file = open('split/training_train_allFiles.csv', 'w')
        training_valid_file = open('split/training_valid_allFiles.csv', 'w')
        training_test_file = open('split/training_test_allFiles.csv', 'w')
        validation_file = open('split/validation_allFiles.csv', 'w')
        testing_file = open('split/testing_allFiles.csv', 'w')
        
        reader = csv.DictReader(csv_file_r)
        fieldnames = ['filename', 'author', 'subreddit', 'title', 'text', 'sentLength', 'timestamp']
        training = csv.DictWriter(training_file, fieldnames=fieldnames)
        training.writeheader()
        training_tr = csv.DictWriter(training_train_file, fieldnames=fieldnames)
        training_tr.writeheader()
        training_va = csv.DictWriter(training_valid_file, fieldnames=fieldnames)
        training_va.writeheader()
        training_te = csv.DictWriter(training_test_file, fieldnames=fieldnames)
        training_te.writeheader()
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
                if r['author'] in author_training_tr:
                    training_tr.writerow(rowinfo)
                elif r['author'] in author_training_va:
                    training_va.writerow(rowinfo)
                elif r['author'] in author_training_te:
                    training_te.writerow(rowinfo)
            elif r['author'] in author_validation:
                validation.writerow(rowinfo)
            elif r['author'] in author_testing:
                testing.writerow(rowinfo)
            else:
                rand = random.random()

                if rand < p_train:
                    author_training[r['author']] = [r['author']]
                    training.writerow(rowinfo)
                    if rand < p_train_tr:
                        author_training_tr[r['author']] = [r['author']]
                        training_tr.writerow(rowinfo)
                    elif rand < (p_train_tr + p_train_va):
                        author_training_va[r['author']] = [r['author']]
                        training_va.writerow(rowinfo)
                    elif rand < (p_train_tr + p_train_va + p_train_te):
                        author_training_te[r['author']] = [r['author']]
                        training_te.writerow(rowinfo)
                elif rand < (p_train + p_validate):
                    author_validation[r['author']] = [r['author']]
                    validation.writerow(rowinfo)
                else:
                    author_testing[r['author']] = [r['author']]
                    testing.writerow(rowinfo)
        csv_file_r.close()
        training_file.close()
        training_train_file.close()
        training_valid_file.close()
        training_test_file.close()
        validation_file.close()
        testing_file.close()
    print("splitData.py Run Time: " + str(time.time()-start_time) + " seconds")
                    
main()          
        