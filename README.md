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

(3b) CONCATERNATE PROCESSED FILES???? combine with 4? -from talking w/ Cate

(4) splitData.py - Splits data into 3 mutually exclusive sets {training (~70\%), validation (~10\%), test (~20\%)} by author
* Reads in the name XXX (in quotes), from (1), which allows the python code to read in the output from (3), i.e. "preprocessed/processed_[XXX].csv"
* Writes to 3 CSV files in a directory called "split"; the created CSV file's name are "training_[XXX].csv" (e.g. "split/training_txtFiles1.csv"), "validation_[XXX].csv" (e.g. "split/validation_txtFiles1.csv"), "testing_[XXX].csv" (e.g. "split/testing_txtFiles1.csv")
>>> python splitData.py "[XXX]"
- Distributes first sentence by a given author into each of the sets (training, validation, test) by corresponding probability value
- Later sentences by the same author are distributed into the same set
- This allows for more matches between critical items ("umm"-containing sentences) and controls

(5) extractUmm.py - Extracts critical "umm"-containing sentences and controls and collects meta data about total and "umm" words and total, "umm"-containing, and control sentences in file
* Reads in the name YYY_XXX (in quotes), where YYY = {training, validation, testing} and XXX is from (1), which allows the python code to read in the output from (4), i.e. "split/[YYY]_[XXX].csv" (e.g. "split/training_txtFiles1.csv")
* Requires nltk
* Writes to a CSV file in a directory called "postExtract"; the created CSV file's name is "sample_[YYY]_[XXX].csv" (e.g. "postExtract/sample_training_txtFiles1.csv")
* Writes to a .txt file in the "postExtract" directory; the created .txt file's name is "metadata_[YYY]_[XXX].txt" (e.g. "postExtract/metadata_training_txtFiles1.csv")
>>> python extractUmm.py "[YYY]_[XXX]"
- Critical "umm"-containing sentences defined as sentences containing a word match to "^umm+$" (e.g. umm, ummmmmmm)
- Control sentences defined as sentences by the same author and the same sentence length as an "umm"-containing sentence
metadata format:
Total Words in File:   ???   total number of words in all posts for a given file
Umm Words in Files:   ???   total number of "umm" words
Total Sentences in File:   ???   total number of sentences
Umm Sentences in File:   ???   total number of critical "umm"-containing sentences
Control Sentences in File:   ???   total number of control sentences
Umm Sentences w/ Control in File:   ???   total number of critical "umm"-containing sentences with at least one control sentence
CSV file
