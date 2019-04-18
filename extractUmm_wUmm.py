#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:24:40 2018

@author: Lauren_Oey
"""

import time
import re
import sys
import csv
import string
csv.field_size_limit(sys.maxsize)
import nltk
from nltk import word_tokenize

authors = dict()
ummControl = dict()
filenames = dict()
count = lambda l1,l2: sum([1 for x in l1 if x in l2])

def main():
    start_time = time.time()
    totalWords = 0
    punct = 0
    ummWords = 0
    totalSentences = 0
    ummSentences = 0
    controlSentences = 0
    ummWithControlSentences = 0

    fileR_name = 'split/'+sys.argv[1]+'_allFiles_concat.csv'

    with open(fileR_name, 'r') as csv_file_r:
        csv_file_w = open('postExtract/wUmm/sample_'+sys.argv[1]+'.csv', 'w')
        reader = csv.DictReader(csv_file_r)
        fieldnames = ['filename', 'author', 'subreddit', 'title', 'lexicalType', 'lexicalItem', 'lexicalLength', 'lexicalIndex', 'text', 'cleanedText', 'newText', 'sentLength', 'timestamp']
        writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
        writer.writeheader()
        meta_file = open('postExtract/wUmm/metadata_'+sys.argv[1]+'.txt', 'w')
        
        for r in reader:
            if r['filename'] not in filenames:
                filenames[r['filename']] = [r['filename']]
                print(r['filename'])

            # recompute sentence length without punctuation
            #noPunct = r['text'].translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            sentSplit = r['cleanedText'].split()
            sentLength = len(sentSplit)

            if sentLength != None:
                totalSentences = totalSentences + 1
                totalWords = totalWords + sentLength
                apos = r['cleanedText'].count("&apos;") #exclude apostrophes
                punctCount = -apos
                for i in sentSplit:
                    if any(x in i for x in string.punctuation):
                        punctCount = punctCount + 1
                punct = punct + punctCount

                # temp sentence that adds spacing between all punctuation
                #punctSent = re.sub("([\\W])",r" \1 ",r['text'])
                #punctSent = punctSent.trim()
                #punctSent = re.sub("\\s{2,}"," ",punctSent)

                # checks for word match to umm and checks that sentence contains more than one word
                if any(re.match("^u(h+|m)m+$", x, re.IGNORECASE) for x in r['cleanedText'].split()) and sentLength > 1:
                    ummSentences = ummSentences + 1

                    # loops through each word in the sentence and finds the word match
                    # used for retrieving the word and the length of the word
                    # records a row in the csv for each word match
                    ind = 0
                    lexItems = []
                    lexLengths = []
                    lexIndices = []
                    newSent = []
                    for w in r['cleanedText'].split():
                        if re.match("^u(h+|m)m+$", w, re.IGNORECASE):
                            lexItems.append(w)
                            lexLengths.append(len(w))
                            lexIndices.append(ind)
                            ummWords = ummWords + 1
                        else:
                            newSent.append(w)
                        ind = ind + 1
                    newSentAsString = " ".join(newSent)
                    for i in range(0,len(lexItems)):
                        writer.writerow({'filename':r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'lexicalType':'umm', 'lexicalItem':lexItems[i], 'lexicalLength':lexLengths[i], 'lexicalIndex':lexIndices[i], 'text':r['text'], 'cleanedText':r['cleanedText'], 'newText':newSentAsString, 'sentLength':sentLength, 'timestamp':r['timestamp']})

                    # checks if comment author exists as an entry in dictionary of authors
                    # if author does not exist, create an entry & sets value to an array containing the length of the sentence
                    if r['author'] not in authors:
                        authors[r['author']] = [str(sentLength)]
                    # if author does exists, but length of sentence is not contained within the array of sentence lengths, adds the length to the array
                    elif str(sentLength) not in authors[r['author']]:
                        authors[r['author']].append(str(sentLength))

                # collects controls
                # checks among non-umm containing sentences if author entry exists and sentence length is contained within the array
                elif r['author'] in authors and str(sentLength) in authors[r['author']]:
                    controlSentences = controlSentences + 1
                    authorLength = r['author'] + ',' + str(sentLength)
                    if authorLength not in ummControl:
                        ummWithControlSentences = ummWithControlSentences + 1
                        ummControl[authorLength] = [authorLength]
                    writer.writerow({'filename':r['filename'], 'author':r['author'], 'subreddit':r['subreddit'], 'title':r['title'], 'lexicalType':'control', 'lexicalItem':'NA', 'lexicalLength':'NA', 'lexicalIndex':'NA', 'text':r['text'], 'cleanedText':r['cleanedText'], 'newText':'NA', 'sentLength':sentLength, 'timestamp':r['timestamp']})

        meta_file.write('Total Words in File: ' + str(totalWords) + "\n")
        meta_file.write('Punctuation in File: ' + str(punct) + "\n")
        meta_file.write("Umm Words in Files: " + str(ummWords) + "\n")
        meta_file.write('Total Sentences in File: ' + str(totalSentences) + "\n")
        meta_file.write('Umm Sentences in File: ' + str(ummSentences) + "\n")
        meta_file.write('Control Sentences in File: ' + str(controlSentences) + "\n")
        meta_file.write('Umm Sentences w/ Control in File: ' + str(ummWithControlSentences))
        meta_file.close()
        csv_file_w.close()
        csv_file_r.close()
    print("extractUmm_wUmm.py Run Time: " + str(time.time()-start_time) + " seconds")

main()
