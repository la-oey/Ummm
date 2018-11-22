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
txtFiles1 (June 2005 - December 2015): 121 GB
txtFiles2 (January 2016 - September 2017): 117 GB
txtFiles3 (October 2017 - August 2018): 100 GB
Test Files - to check run time with subset of data
test1GB (April 2012): 998 MB
test10GB (May 2018): 9.9 GB

1) Extracts raw text comments, tokenizes comments at sentence level, and extracts select meta info from reddit text files, and convert to CSV files in rawtxt directory
XXX = txtFiles{1, 2, 3} or text{1, 10}GB
python extractRawTxt.py [XXX]
Creates file "rawtxt/raw_[XXX].csv"
CSV file: {
	filename,
	author: reddit['author'],
	subreddit: reddit['subreddit'],
	title: reddit['title'],
	text: nltk.sent_tokenize(reddit['selftext']),
	timestamp: reddit['created_utc']}

2) Preprocesses sentences
- Removes sentences with "NA", "[deleted], "[removed]" as the text
- Removes sentences with "[deleted]", "autotldr", and ending in "bot" (e.g. "frontbot", "removalbot")
- Uses langid package to remove non-English sentences
- Removes text starting with "http(s)://" or "www."
- Removes "_"
- Removes non-ASCII characters using HTMLParser().unescape()
- Tokenizes words and converts characters to lower-case
- Rejoins words with whitespace
Writes preprocessed sentences (with meta data) to a new CSV file

3) Splits data into 3 mutually exclusive sets {training (50\%), validation (10\%), test (40\%)}

