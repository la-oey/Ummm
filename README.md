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
txtFiles0 (June 2005 - April 2015): 86 GB
txtFiles1 (May 2015 - October 2016): 86  GB
txtFiles2 (November 2016 - November 2017): 81 GB
txtFiles3 (December 2017 - August 2018): 86 GB
Test Files - to check run time with subset of data (directories not currently existing)
1GB (April 2012): 998 MB
10GB (May 2018): 9.9 GB

(1) extractRawTxt.py - Extracts raw text comments, tokenizes comments at sentence level, and extracts select meta info from reddit text files, and convert to CSV files in rawtxt directory
* Reads in the name XXX of a directory with .txt files from the Reddit corpus (e.g. "txtFiles1")
* Requires nltk
* Writes to a CSV file in a directory called "rawtxt"; the created CSV file's name is "raw_[XXX].csv" (e.g. "rawtxt/raw_txtFiles1.csv")
\>\>\> python extractRawTxt.py [XXX]
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
\>\>\> python getRedditBots.py

(3) preprocessingTraining.py - Preprocesses sentences
* Reads in the name XXX (in quotes), from (1), which allows the python code to read in the output from (1), i.e. "rawtxt/raw_[XXX].csv"
* Reads in "redditbots.txt"
* Reads in "lid.176.ftz" (for pyfasttext)
* Requires nltk, HTMLParser, pyfasttext
* Writes to a CSV file in a directory called "preprocessed"; the created CSV file's name is "processed_XXX.csv" (e.g. "preprocessed/processed_txtFiles1.csv")
\>\>\> python preprocessingTraining.py [XXX]
- Excludes sentences with "NA", "[deleted], "[removed]" as the text
- Excludes authors named "[deleted]", "autotldr", "peterboykin", "censorship_notifier", "AutoModerator", "subredditreports", and "scamcop"
- Excludes (bot) authors listed in "redditbots.txt"
- Excludes authors whose name ends in "bot" (ignore case) (e.g. "frontbot", "removalbot")
- Uses pyfasttext package to exclude non-English sentences
- Excludes text starting with "http(s)://" or "www."
- Removes "_"
- Removes non-ASCII characters using HTMLParser().unescape()
- Tokenizes words to compute the word length (note: we are no longer converting words to lower case)

(4) concatenate.sh - Concatenates all of the preprocessing CSV files into a single CSV file
* Reads in all files in the "preprocessed" directory
* Writes to a CSV file called "preprocessed/processed_allFiles.csv"
\>\>\> chmod +x concatenate.sh
\>\>\> ./concatenate.sh
- Writes header of the first file in the directory
- Concatenates all of the rows from the CSV files into a single CSV file

(5) splitData.py - Splits data into 3 mutually exclusive sets {training (~8\%), training_valid (~1\%), training_test (~1\%), validation (~45\%), testing (~45\%)} by author
* Reads in the "preprocessed/processed_allFiles.csv", created in (4)
* Writes to 5 CSV files: "split/training_allFiles.csv", "split/training_valid_allFiles.csv", "split/training_test_allFiles.csv", "split/validation_allFiles.csv", "split/testing_allFiles.csv"
\>\>\> python splitData.py
- Distributes first sentence by a given author into each of the sets (training, validation, test) by corresponding probability value
- Later sentences by the same author are distributed into the same set
- This allows for more matches between critical items ("umm"-containing sentences) and controls
- Training set size decided because of limitations in awd-lstm-lm's capacity to train on a larger data set





# kenlm: LM trained on reddit data or pre-trained on CommonCrawl data #

(6a) writeTrainingTxt_kenlm.py - If training the LM on your own data, extracts text in training CSV file to text file
* Reads in "split/training_allFiles.csv" (output from 5)
* Writes to text file "trainingTxt_allFiles.txt"
\>\>\> python writeTrainingTxt_kenlm.py
- Extracts vector containing the relevant text in the training CSV file
- Writes each sentence to the text file, separated by a newline
- Then preprocess using kenlm_prepro
\>\>\> cd kenlm_prepro
\>\>\> cat ../trainingTxt_allFiles.txt | ./prepro_post_dedupe_en.sh en | ./prepro_tokenize_en.sh en truecasemodels/truecase-model.en > ../trainingTxt_allFiles.txt

(6b) kenlm - Builds a 5-gram language model
from https://kheafield.com/code/kenlm/
github: https://github.com/kpu/kenlm
* Reads in "trainingTxt_allFiles.txt" created in (7a) from its directory
* Writes binary file that can be used to query the model
(i) If kenlm not set up, use the following commands:
\>\>\> wget -O - https://kheafield.com/code/kenlm.tar.gz | tar xz
\>\>\> mkdir kenlm/build
\>\>\> cd kenlm/build
\>\>\> cmake ..
\>\>\> make -j2
(ii) Once kenlm is set up, use:
\>\>\> bin/lmplz -o 5 -S 80\% -T /tmp <../trainingTxt_allFiles.txt >reddit.arpa
\>\>\> bin/build_binary reddit.arpa reddit.binary

(6c) sentToTxt.py - Extracts and creates unique corresponding indices for each sentence across two generated files
* Reads in the name YYY, where YYY = {training, training_valid, training_test, validation, testing}, which allows the python code to read in the output from (4), i.e. "split/[YYY]_allFiles.csv" (e.g. "split/testing_allFiles.csv")
* Writes to 2 CSV files in the "split/" directory: (a) a file with all of the data, plus unique numeric indices "split/[YYY]_allFiles_full.csv" (e.g. "split/testing_allFiles_full.csv"), (b) a file with the unique indices and the text, extracted "split/[YYY]_allFiles_txt.csv" (e.g. "split/testing_allFiles_txt.csv")
\>\>\> python sentToTxt.py [YYY]
YYY = {training, training_valid, training_test, validation, testing}

(6d) kenlm_prepro - Files for kenlm preprocessing
* Reads in "split/[YYY]_allFiles_txt.csv" file from (7b)
* Change directory to "kenlm_prepro/"
* Writes to a CSV file after preprocessing for kenlm "../split/[YYY]_allFiles_cleaned.csv"
\>\>\> cd kenlm_prepro
\>\>\> cat ../split/[YYY]_allFiles_txt.csv | ./prepro_post_dedupe_en.sh en | ./prepro_tokenize_en.sh en truecasemodels/truecase-model.en > ../split/[YYY]_allFiles_cleaned.csv
YYY = {training, training_valid, training_test, validation, testing}
- Adds spacing between punctuation
- Converts some characters to HTML character, e.g. " --> &quot;

(6e) concat_kenlm_post-prepro.py - Concatenates full file from (7b) and preprocessed file from (7c)
* Reads in "split/[YYY]_allFiles_full.csv" file from (7b) and "split/[YYY]_allFiles_cleaned.csv" file from (7c)
* Change to back to "Ummm/" directory
* Writes to a CSV file "split/[YYY]_allFiles_concat.csv"
\>\>\> cd ..
\>\>\> python concat_kenlm_post-prepro.py [YYY]
- Strips extra spaces around "index" column of CSV
- Works around some odd formatting issues, e.g. extra "None" columns, rows consisting of cleaned text without indices, rows with indices but no text
- Concatenates files into a single file

(6f(a)) extractUmm_wUmm.py - Extracts critical "umm"-containing sentences and controls and collects meta data about total and "umm" words and total, "umm"-containing, and control sentences in file
* Reads in the name YYY, where YYY = {training, validation, testing}, which allows the python code to read in the output from (4), i.e. "split/[YYY]_allFiles.csv" (e.g. "split/testing_allFiles.csv")
* Requires nltk
* Writes to a CSV file in a directory called "postExtract/wUmm/"; the created CSV file's name is "sample_[YYY].csv" (e.g. "postExtract/wUmm/sample_testing.csv")
* Writes to a .txt file in the "postExtract/wUmm/" directory; the created .txt file's name is "metadata_[YYY].txt" (e.g. "postExtract/wUmm/metadata_testing.csv")
\>\>\> python extractUmm_wUmm.py [YYY]
YYY = {training, training_valid, training_test, validation, testing}
- Re-computes sentence length (without punctuation), which prevents issues of "a...b" counting as one word
- Creates temporary sentence with spaces between each punctuation, which is used to extract umm sentences, which prevents issues of "a...umm" not being extracted
- Critical "umm"-containing sentences defined as sentences containing a word match to "^u(h+|m)m+$" (e.g. umm, ummmmmmm, UMMM, uhmm)
- Excluded sentences containing only 1 word
- Edited "umm"-containing sentences (punctuation separated by spaces) to exclude "umm" words (appended edited sentence to newText column)
- Control sentences defined as sentences by the same author and the same sentence length as an "umm"-containing sentence, minus "ummm" words
metadata format:
Total Words in File:   11,114,557,558   total number of words in all posts for a given file
Umm Words in Files:   40,880   total number of "umm" words
Total Sentences in File:   671,555,076   total number of sentences
Umm Sentences in File:   40,163   total number of critical "umm"-containing sentences
Control Sentences in File:   859,344   total number of control sentences
Umm Sentences w/ Control in File:   23,936   total number of critical "umm"-containing sentences with at least one control sentence
CSV file: {
	filename: from (1),
	author: from (1),
	subreddit: from (1),
	title: from (1),
	lexicalType: {umm, control},
	lexicalItem: {umm token (e.g. umm, ummmmmm), NA},
	lexicalLength: {character length of umm token (e.g. 3+), NA},
	lexicalIndex: index of "umm" in original text (zero-based),
	text: original text,
	newText: {original text minus "umm" words, NA}
	sentLength: sentence length,
	timestamp: from (1)}

(6f(b)) extractUmm_woUmm.py - Extracts critical "umm"-containing sentences and controls and collects meta data about total and "umm" words and total, "umm"-containing, and control sentences in file
* Reads in the name YYY (in quotes), where YYY = {training, validation, testing}, which allows the python code to read in the output from (4), i.e. "split/[YYY]_allFiles.csv" (e.g. "split/testing_allFiles.csv")
* Requires nltk
* Writes to a CSV file in a directory called "postExtract/woUmm/"; the created CSV file's name is "sample_[YYY].csv" (e.g. "postExtract/woUmm/sample_testing.csv")
* Writes to a .txt file in the "postExtract/woUmm/" directory; the created .txt file's name is "metadata_[YYY].txt" (e.g. "postExtract/woUmm/metadata_testing.csv")
\>\>\> python extractUmm_woUmm.py [YYY]
YYY = {training, training_valid, training_test, validation, testing}
- Critical "umm"-containing sentences defined as sentences containing a word match to "^([\\W]*)u(h+|m)m+([\\W]*)$" (e.g. umm, ummmmmmm, UMMM, uhmm, ...umm..., "umm")
- Excluded sentences containing only 1 word
- Edited "umm"-containing sentences to exclude "umm" words (retained original sentence in originalText column)
- Control sentences defined as sentences by the same author and the same sentence length as an "umm"-containing sentence, minus "ummm" words
metadata format:
Total Words in File:   11,114,557,558   total number of words in all posts for a given file
Umm Words in Files:   40,880   total number of "umm" words
Total Sentences in File:   671,555,076   total number of sentences
Umm Sentences in File:   40,163   total number of critical "umm"-containing sentences
Control Sentences in File:   823,554   total number of control sentences
Umm Sentences w/ Control in File:   23,716   total number of critical "umm"-containing sentences with at least one control sentence
CSV file: {
	filename: from (1),
	author: from (1),
	subreddit: from (1),
	title: from (1),
	lexicalType: {umm, control},
	lexicalItem: {umm token (e.g. umm, ummmmmm), NA},
	lexicalLength: {character length of umm token (e.g. 3+), NA},
	lexicalIndex: index of "umm" in original text (zero-based),
	originalText: {original text, NA},
	text: original text minus "umm" words,
	sentLength: sentence length minus "umm" words,
	timestamp: from (1)}

(6g) test_kenlm.py - Queries language model for surprisal with critical "umm"-containing and control sentences
* Reads in "postExtract/sample_[YYY].csv" created in (6a) (e.g. "postExtract/wUmm/sample_testing.csv") or (6b) (e.g. "postExtract/woUmm/sample_testing.csv")
* Requires kenlm python package
* Either queries the data extracted with ("w") umm (6a) or without ("wo") umm (6b) AAA = {w, wo}
* Either queries reddit-trained or CommonCrawl-trained data BBB = {reddit, crawl}
* Writes to a CSV file "umm_kenlm_output_[YYY].csv"
\>\>\> python test_kenlm.py [YYY] [AAA] [BBB]
- Initial run through takes awhile because it is training the model
- Sequential run throughs are much faster (~20 seconds total)
- Outputs log10(probability(word|prev words)) for each sentence from kenlm model in "kenlm_output" vector
- Outputs log10(probability(word|prev words)) as list for each word in sentence
(reddit) If querying the reddit data-trained LM, use "reddit" as the second argument in the command
(crawl) Worried about overfitting the LM due to the low overall frequency of "umm" words in the training data, we used a pre-trained kenlm LM that had been trained on 35.2 TB of data from CommonCrawl.com (http://statmt.org/ngrams/). Use "crawl" as second argument
To download pretrained LM:
* Requires xz-utils
\>\>\> wget http://data.statmt.org/ngrams/lm/en.trie.xz
\>\>\> unxz en.trie.xz
- kenlm preprocessing script provided here: http://data.statmt.org/ngrams/prepro.tgz

# LSTM: LM trained on reddit data or trained on enwik-8 #

(7a) writeTrainingTxt_lstm.py - If training the LM on your own data, extracts text in training CSV file to text file
* Reads in "split/[YYY]_allFiles.csv" where YYY = {"training", "training_valid", "training_test"} (output from 5)
* Writes to a text file {"train.txt", "valid.txt", "test.txt"} in the "redditTrain/" directory (e.g. "redditTrain/test.txt")
\>\>\> python writeTrainingTxt_lstm.py [YYY]
- Extracts vector containing the relevant text in the training CSV file
- Writes each sentence to the text file, separated by a newline

(7b) awd-lstm-lm - Builds character level long short-tern memory network (LSTM) language model
* Reads in "redditTrain/" created in (8a) from its directory
* Requires PyTorch 0.4
* Writes binary file that can be used to query the model
(i) If awd-lstm-lm not set up, do the following:
- To acquire datasets that the repository comes with instructions to train
\>\>\> ./getdata.sh
(ii) Once awd-lstm-lm is set up, use:
(reddit) To train LSTM on reddit data:
* Reads in directory "data/redditTrain/"
* Writes to "REDDIT.pt", "REDDIT.pt.e25", "REDDIT.pt.e35"
\>\>\> ../anaconda3/bin/python3 -u main.py --epochs 50 --nlayers 3 --emsize 400 --nhid 1840 --alpha 0 --beta 0 --dropoute 0 --dropouth 0.1 --dropouti 0.1 --dropout 0.4 --wdrop 0.2 --wdecay 1.2e-6 --bptt 200 --batch_size 128 --optimizer adam --lr 1e-3 --data data/redditTrain --save REDDIT.pt --when 25 35
NOTE: NEEDS TO BE ADJUSTED
(enwik-8) To train LSTM on enwik-8 data:
* Reads in directory "data/enwik8/"
* Writes to "ENWIK8.pt", "ENWIK8.pt.e25", "ENWIK8.pt.e35"
\>\>\> ../anaconda3/bin/python3 -u main.py --epochs 50 --nlayers 3 --emsize 400 --nhid 1840 --alpha 0 --beta 0 --dropoute 0 --dropouth 0.1 --dropouti 0.1 --dropout 0.4 --wdrop 0.2 --wdecay 1.2e-6 --bptt 200 --batch_size 128 --optimizer adam --lr 1e-3 --data data/enwik8 --save ENWIK8.pt --when 25 35


# Data Analysis #

(8) suprisalAnalysis.Rmd - Data analysis of surprisal
* Reads in "umm_[ZZZ]_output_[YYY].csv" where YYY = {"training", "validation", "testing"} and ZZZ = {"kenlm", "lstm"}
* Creates PDF of cleaning, visualization, and data analysis
\>\>\> knit to PDF
- All critical "umm" sentences have a corresponding control sentence matched for author and sentence length (excluding "umm" word(s))
- Dependent measures:
(1) Surprisal of overall sentence
(2) Surprisal of sentence before critical lexical index (pre-umm)
(3) Surprisal of sentence after critical lexical index (post-umm)
(4) Surprisal of sentence after critical lexical index minus surprisal of sentence before critical lexical index (difference)
Cleaning
- Applied "umm" sentence index to corresponding control sentences (controlled for author and sentence length)
- When an author for a given sentence length had more than one "umm" sentence with different sentence indices, applied all of the indices to the multiple corresponding control sentences
- Excluded critical items without a corresponding control
- Instead of log probability (outputted by kenlm), used negative log probability
- Converted base zero indexing to base one indexing
- Excluded sentences in which the sentence index ("umm" and control) is in the first, second, or last position in the sentence
Visualizations
- Each "point" in the violin plot is surprisal averaged over all instances of critical or control sentences for a given author, sentence length, and sentence index
- Visualized pre-umm and post-umm surprisal by differences in number of words before and after "ummm"
- Visualized sentence-level, pre-umm, post-umm, and difference (post-pre) in "umm" length where the minimum was 3 (e.g. "umm") and maximum was 6 (needed to distribution "umm" length over controls if there were multiple matched for author, sentence length, and sentence index)
Analysis
