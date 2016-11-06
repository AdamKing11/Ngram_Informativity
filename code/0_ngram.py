import re, sys, math

def ngram_informativity(ngrams):
	"""
	takes in an ngram file and calculates average informativy
	informativity is defined as - AVG LOG prob of word | context
	in this case, the "word" is the final word in the ngram
	and the "context" is all words before it:

	"""

	context = ()
	context_competitors = {}
	context_counts = {}
	informativity = {}
	comp_sum = 0
	# first thing to do is SORT 
	# we're sorting the ngram keys by the first part of the ngrams
	# (we don't really care about the last guy)
	
	c = 0
	
	print("We have", len(ngrams),"total ngrams to look at...")
	for g in sorted(ngrams, key = lambda element: tuple(element[:-1])):
		c+=1
		print("Looking at",c, end="\r")
		# if we're in a new context....
		if tuple(g[:-1]) != context:
			for w in context_competitors:
				# okay, so we take the ngram count for the given word and 
				# divide it by the total sum of ALL ngrams of the same context
				# then, take log2 (to prevent underflow)
				##
				# we also store a count of how many times we've touched the 
				# informativity for each word so we can get the avg later
				if w in informativity:
					informativity[w] += math.log(context_competitors[w]/comp_sum,2)
					context_counts[w] += 1
				else:
					informativity[w] = math.log(context_competitors[w]/comp_sum,2)
					context_counts[w] = 1
			context = tuple(g[:-1])
			context_competitors = {}
			context_sum = 0
			
		# otherwise, just add it to running list of counts and competetors
		# in the context
		
		# a little opaque but this is adding the total count for the 
		# ngram into a dictionary for the context where the current 
		# word is the key
		context_competitors[g[-1]] = ngrams[g]
		# just make a variable to store the SUM of all competitors so far
		comp_sum += ngrams[g]
	print("\nDone. Getting averages....")
	# okay, we've gone through the ngrams -- let's get the average for each
	for g in informativity:
		informativity[g] /= -context_counts[g]
		pass

	print("the", context_counts["the"])
	print("consequences", context_counts["consequences"])
	return informativity

def build_ngrams(coca_file, ngram_size=2):
	"""
	Opens a file an builds a dictionary of ngrams of a given length

	"""
	ngram_d = {}

	c = 0
	with open(coca_file, "r") as rF:
		for line in rF:
			c += 1
			print("Reading line", c, end="\r")
			words = clean_line(line).split(" ")
			# we're going to loop through all words and build ngrams out of them
			# because ngrams are "sliding windows", we start at the beginning and
			# go to the last - (ngram_size-1) (i.e. in trigrams, we stop at end - 2)
			# 
			for i in range(len(words)-(ngram_size-1)):
				# make the ngram into a tuple (to use as key in dict)
				ngram = tuple(words[i:i+ngram_size])

				# check to make sure ALL words are good in the ngram
				if good_ngram(ngram):
					if ngram in ngram_d:
						ngram_d[ngram] += 1
					else:
						ngram_d[ngram] = 1
	print("\nDone reading.", c, "lines read in total.")
	return ngram_d

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
	if len(w) == 0:
		return False

	if re.search("^[:@.,\"]",w):
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
		"'m")

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
	w = re.sub("(^[\-\.]|[\-\.]$)","",w)
	return(w)


if __name__ == "__main__":
	# use the first argument as the COCA (or smaller version) to 
	# calc everything
	b = build_ngrams(sys.argv[1],4)

	print("\n10 most frequent ngrams:")
	for n in sorted(b, key = lambda g: b[g], reverse=True)[:10]:
		print(n,b[n])

	i = ngram_informativity(b)

	print("\n10 most informative words:")
	for n in sorted(i, key = lambda g: i[g], reverse=True)[:10]:
		print("\t", n,i[n])
	
	print("\n10 least informative words:")
	for n in sorted(i, key = lambda g: i[g])[:10]:
		print("\t", n,i[n])
	