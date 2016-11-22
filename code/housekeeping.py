import re

# file for holding all the functions for cleaning up the data

def good_ngram(n):
	"""
	takes an ngram and checks to make sure all words are good
	"""
	for w in n:
		if not good_word(w):
			return False
	return True

def good_word(w):
	"""
	takes a word and checks if we want to keep track of it
	like, some junk in COCA is just noise
	"""

	# we want to exclude punctuation
	# the way this works is that it will FORCE us to 
	# keep moving the 'sliding window' until we're past the
	# punctuation -> so that "big . Blue" is not saved as a 
	# trigram
	punc = "\&!\?:@\.,\"\\\/\$\'\%\)\(\*\#+"
	punc = re.compile("^[" + punc + "]")

	if len(w) == 0:
		return False

	if re.search(punc,w):
		return False

	# COCA has names of speakers in CAPS
	if w == w.upper() and len(w) > 1:
		return False

	return True

def clean_line(line):
	"""
	takes a line of text and returns a "cleaned" form of the line
	
	"""

	# the way COCA does it is is to split ""contractions"" into 
	# separate words, we'll just plop them on the previous word
	contractions = ("n't", "'re", "'s", "'me",
		"'m", "'ll", "'ve", "'d")

	l = line.rstrip().rsplit(" ")
	line = ""
	for w in l:
		cw = clean_word(w)
		# because COCA makes n't separate words
		if cw in contractions:
			line = line[:-1] + cw + " "
		else:
			line += cw + " "

	return(line[:-1])

def clean_word(w):
	"""
	takes a word and "cleans" it, ie folds case and gets rid of weird stuff
	"""
	w = w.lower()
	w = re.sub("(^[\-\.]|[\-\.;,]$)","",w)
	return(w)

def preprocess_COCA():
	"""
	preprossessing - we take in COCA, run EVERYTHING through
	# the clean_line fucntion and save the result - so we don't
	# need to do it everytime we run
	
	"""
	print("***PREPROCESSING COCA***")
	print("We're going to open up the COCA file and clean it", \
		"up so we don't need to do that for every run.")

	rF = open("COCA.cat.txt", "r")
	wF = open("COCA.clean.txt", "w")

	i = 0
	for line in rF:
		i+=1
		print("Doing line", i, end="\r")
		wF.write(clean_line(line) + "\n")

	rF.close()
	wF.close()
