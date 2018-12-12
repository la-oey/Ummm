# Ummm

An analysis of "umm" in text-based communication (reddit corpus).
Collects frequency statistics from the corpus and compares the surprisal of sentences containing "umm" and their controls (i.e. sentences written by the same author and of the same length).

Full Reddit Corpus as of 10/23/2018
Each month is contained within a single text file.
Lines in text file correspond to each post and each post consists of a dictionary:
{"archived", "author","is_self", "author_flair_css_class", "author_flair_text", "created", "created_utc", "distinguished", "domain", "downs", "edited", "from", "from_id", "from_kind", "gilded", "hide_score", "id", "link_flair_css_class", "link_flair_text", "media", "media_embed", "name", "num_contents", "over_18", "permalink", "retrieved_on", "quarantine", "saved", "score", "secure_media", "secure_media_embed", "selftext", "stickied", "subreddit", "subreddit_id", "thumbnail", "title", "ups", "url"}

Corpus approximately split into thirds (by GB) in different directories
Directories and text files hosted on Leon's server

Total (June 2005 - August 2018): 338 GB
txtFiles0 (June 2005 - September 2014): 65 GB
txtFiles1 (October 2014 - December 2015): 57  GB
txtFiles2 (January 2016 - September 2017): 117 GB
txtFiles3 (October 2017 - August 2018): 100 GB
Test Files - to check run time with subset of data (directories not currently existing)
1GB (April 2012): 998 MB
10GB (May 2018): 9.9 GB

(1) extractRawTxt.py - Extracts raw text comments, tokenizes comments at sentence level, and extracts select meta info from reddit text files, and convert to CSV files in rawtxt directory
* Reads in the name XXX (in quotes) of a directory with .txt files from the Reddit corpus (e.g. "txtFiles1")
* Requires nltk
* Writes to a CSV file in a directory called "rawtxt"; the created CSV file's name is "raw_[XXX].csv" (e.g. "rawtxt/raw_txtFiles1.csv")
>>> python extractRawTxt.py "[XXX]"
XXX = txtFiles{0, 1, 2, 3}
CSV file: {
	filename,
	author: reddit['author'],
	subreddit: reddit['subreddit'],
	title: reddit['title'],
	text: nltk.sent_tokenize(reddit['selftext']),
	timestamp: reddit['created_utc']}

(2) getRedditBots.py - Writes list of bot names to "redditbots.txt" file
* Reads in redditbots-autowikibot.htm, an html file to https://www.reddit.com/r/autowikibot/wiki/redditbots
* Requires bs4 (BeautifulSoup)
* Writes list of extracted bot names, each separated by a new line, to "redditbots.txt"
>>> python getRedditBots.py

(3) preprocessingTraining.py - Preprocesses sentences
* Reads in the name XXX (in quotes), from (1), which allows the python code to read in the output from (1), i.e. "rawtxt/raw_[XXX].csv"
* Reads in "redditbots.txt"
* Requires nltk, HTMLParser, langid
* Writes to a CSV file in a directory called "preprocessed"; the created CSV file's name is "processed_XXX.csv" (e.g. "preprocessed/processed_txtFiles1.csv")
>>> python preprocessingTraining.py "[XXX]"
- Removes sentences with "NA", "[deleted], "[removed]" as the text
- Removes (bot) authors listed in "redditbots.txt"
- Removes authors with "[deleted]", "autotldr", and ending in "bot" (e.g. "frontbot", "removalbot")
- Uses langid package to remove non-English sentences
- Removes text starting with "http(s)://" or "www."
- Removes "_"
- Removes non-ASCII characters using HTMLParser().unescape()
- Tokenizes words and converts characters to lower-case
- Rejoins words with whitespace

(4) concatenate.sh - Concatenates all of the preprocessing CSV files into a single CSV file
* Reads in all files in the "preprocessed" directory
* Writes to a CSV file called "preprocessed/processed_allFiles.csv"
>>> chmod +x concatenate.sh
>>> ./concatenate.sh
- Writes header of the first file in the directory
- Concatenates all of the rows from the CSV files into a single CSV file

(5) splitData.py - Splits data into 3 mutually exclusive sets {training (~35\%), validation (~35\%), test (~30\%)} by author
* Reads in the "preprocessed/processed_allFiles.csv", created in (4)
* Writes to 3 CSV files: "split/training_allFiles.csv", "split/validation_allFiles.csv", "split/testing_allFiles.csv"
>>> python splitData.py
- Distributes first sentence by a given author into each of the sets (training, validation, test) by corresponding probability value
- Later sentences by the same author are distributed into the same set
- This allows for more matches between critical items ("umm"-containing sentences) and controls
- Training set size decided because of limitations in kenlm capacity to train on a larger data set

(6) writeTrainingTxt.py - Extracts text in training CSV file to text file
* Reads in "split/training_allFiles.csv"
* Writes to text file "trainingTxt_allFiles.txt"
>>> python writeTrainingTxt.py
- Extracts vector containing the relevant text in the training CSV file
- Writes each sentence to the text file, separated by a newline

(7) kenlm - Builds binary file for unpruned language model estimation
from https://kheafield.com/code/kenlm/
github: https://github.com/kpu/kenlm
* Reads in "trainingTxt_allFiles.txt" created in (6) from its directory
* Writes binary file that can be used to query the model
(a) If kenlm not set up, use the following commands:
>>> wget -O - https://kheafield.com/code/kenlm.tar.gz |tar xz
>>> mkdir kenlm/build
>>> cd kenlm/build
>>> cmake ..
>>> make -j2
(b) Once kenlm is set up, use:
>>> bin/lmplz -o 5 -S 80\% -T /tmp <../trainingTxt_allFiles.txt >reddit.arpa
>>> bin/build_binary reddit.arpa reddit.binary

(8) extractUmm.py - Extracts critical "umm"-containing sentences and controls and collects meta data about total and "umm" words and total, "umm"-containing, and control sentences in file
* Reads in the name YYY (in quotes), where YYY = {training, validation, testing}, which allows the python code to read in the output from (4), i.e. "split/[YYY]_allFiles.csv" (e.g. "split/testing_allFiles.csv")
* Requires nltk
* Writes to a CSV file in a directory called "postExtract"; the created CSV file's name is "sample_[YYY]_allFiles.csv" (e.g. "postExtract/sample_testing_allFiles.csv")
* Writes to a .txt file in the "postExtract" directory; the created .txt file's name is "metadata_[YYY]_allFiles.txt" (e.g. "postExtract/metadata_testing_allFiles.csv")
>>> python extractUmm.py "[YYY]"
YYY = {training, validation, testing}
- Critical "umm"-containing sentences defined as sentences containing a word match to "^umm+$" (e.g. umm, ummmmmmm)
- Control sentences defined as sentences by the same author and the same sentence length as an "umm"-containing sentence
metadata format:
Total Words in File:   11,576,342,718   total number of words in all posts for a given file
Umm Words in Files:   39,429   total number of "umm" words
Total Sentences in File:   685,388,022   total number of sentences
Umm Sentences in File:   35,899   total number of critical "umm"-containing sentences
Control Sentences in File:   821,361   total number of control sentences
Umm Sentences w/ Control in File:   19,831   total number of critical "umm"-containing sentences with at least one control sentence
CSV file: {
	filename: from (1),
	author: from (1),
	subreddit: from (1),
	title: from (1),
	lexicalType: {umm, control},
	lexicalItem: {umm token (e.g. umm, ummmmmm), NA},
	lexicalLength: {character length of umm token (e.g. 3+), NA},
	text: from (3) (prerprocessed text),
	sentLength: sentence length,
	timestamp: from (1)}

(9) kenlm_test.py - Queries language model for surprisal with critical "umm"-containing and control sentences
* Reads in "postExtract/sample_[YYY]_allFiles.csv" created in (8) (e.g. "postExtract/sample_testing_allFiles.csv")
* Requires kenlm python package
* Writes to a CSV file "umm_kenlm_output_[YYY].csv"
>>> python test_kenlm.py "[YYY]"
- Initial run through takes awhile because it is training the model
- Sequential run throughs are much faster (~20 seconds total)
- Outputs log10(probability(word|prev words)) for each sentence from kenlm model in "kenlm_output" vector
- Outputs log10(probability(word|prev words)) as list for each word in sentence

(10) suprisalAnalysis.Rmd - Data analysis of surprisal
* Reads in "Umm_kenlm_output_[YYY].csv"
* Creates PDF of cleaning, visualization, and data analysis
>>> knit to PDF
- All critical "umm" sentences have a corresponding control sentence matched for author and sentence length
- Dependent measures:
(1) Surprisal of sentence after critical lexical index
Cleaning
-
Visualizations
- Each point is surprisal averaged over all instances of critical or control sentences for a given author and sentence length
- In (2) and (3), for instances in which there are m
Analysis



