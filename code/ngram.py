import re, sys, math

from code.housekeeping import *

# meat and potatoes




def ngram_informativity(ngrams):
	"""
	takes in an ngram file and calculates average informativy
	informativity is defined as - AVG LOG prob of word | context
	in this case, the "word" is the final word in the ngram
	and the "context" is all words before it:

	'ngrams' is a dictionary where the KEYS are tuples for each part
	of the ngram

	"""

	context = ()
	context_competitors = {}
	context_counts = {}
	informativity = {}
	context_sum = 0
	# first thing to do is SORT 
	# we're sorting the ngram keys by the first part of the ngrams
	# (we don't really care about the last guy)
	
	c = 0
	# we add this terminal item as the LAST item we loop through
	# this way, we can ENSURE we update the final time
	terminal_item = "ZZZZZ"
	
	print("We have", len(ngrams),"total ngrams to look at...")
	# sort by all but last thing in the tuple
	sorted_ngrams = sorted(ngrams, key = lambda elements: tuple(elements[:-1]))
	sorted_ngrams.append(terminal_item)

	for g in sorted_ngrams:
		c+=1
		print("Looking at",c, end="\r")
		# if we're in a new context OR we're at the end....
		if tuple(g[:-1]) != context or g == terminal_item:
			for w in context_competitors:
				# okay, so we take the ngram count for the given word and 
				# divide it by the total sum of ALL ngrams of the same context
				# then, take log2 (to prevent underflow)
				##
				# we also store a count of how many times we've touched the 
				# informativity for each word so we can get the avg later
				if w in informativity:
					informativity[w] += math.log(context_competitors[w]/context_sum,2)
					context_counts[w] += 1
				else:
					informativity[w] = math.log(context_competitors[w]/context_sum,2)
					context_counts[w] = 1
			# if we got here via the terminal item, end the loop here
			if g == terminal_item:
				break
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
		context_sum += ngrams[g]
	
	print("\nDone. Getting averages....")
	# okay, we've gone through the ngrams -- let's get the average for each
	for g in informativity:
		informativity[g] /= -context_counts[g]

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
			
			######
			# pre-processing takes out need to clean the line every time
			######
			#words = clean_line(line).split(" ")
			words = line.rstrip().split(" ")

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

def save_ngram_file(ngrams, outfile = None):
	"""
	save the ngrams we generated
	format will be: ngram TAB count
		with all words in ngram separated by SPACE
		(so we can tell them apart....)
	"""


	# sort the ngrams
	ngram_list = sorted(ngrams, key = lambda element: tuple(element[:-1]))
	ngram_len = len(ngram_list[0])

	# give it a default name if we don't have one yet
	if outfile == None:
		outfile = str(ngram_len) + "-grams.txt"

	with open(outfile, "w") as wF:
		for n in ngram_list:
			ngram_str = ""
			for w in n:
				ngram_str += w + " "
			ngram_str = ngram_str[:-1]
			wF.write(ngram_str + "\t" + str(ngrams[n]) + "\n")

def load_ngram_file(ngram_file):
	"""
	loads in an already created ngram file and returns it
	"""
	ngrams = {}
	i = 0
	print("Opening", ngram_file, "....")
	with open(ngram_file, "r") as rf:
		for line in rf:
			i+=1
			print("Reading line", i, end="\r")
			line = line.rstrip().rsplit("\t")
			n = tuple(line[0].rsplit(" "))
			count = int(line[1])
			ngrams[n] = count
	print("\nDone reading", i, "ngrams.")
	return ngrams

def save_informativity_file(infor, outfile = "avg_informativity.txt"):
	"""
	format - word TAB informativity
	"""

	with open(outfile, "w") as wF:
		for i in sorted(infor):
			wF.write(i + "\t" + str(infor[i]) + "\n")


if __name__ == "__main__":

	# only do this the first time you run, afterwards,
	# it should run much faster
	should_preprocess = False

	if should_preprocess:
		preprocess_COCA()
		print()
		sys.exit(0)

	ngram_size = 2


	# use the first argument as the COCA (or smaller version) to 
	# calc everything
	b = build_ngrams("COCA.clean.txt",ngram_size)

	print("Done making n-grams. Saving....")
	save_ngram_file(b, str(ngram_size)+"-gram.txt")

	print("\n10 most frequent ngrams:")
	for n in sorted(b, key = lambda g: b[g], reverse=True)[:10]:
		print(n,b[n])

	i = ngram_informativity(b)
	# clear memory of the ngrams, we've already used and saved them
	b = []
	print("Done calculating informativity. Saving....")
	save_informativity_file(i, str(ngram_size)+"-gram.informativity.txt")

	print("\n10 most informative words:")
	for n in sorted(i, key = lambda g: i[g], reverse=True)[:10]:
		print("\t", n,i[n])
	
	print("\n10 least informative words:")
	for n in sorted(i, key = lambda g: i[g])[:10]:
		print("\t", n,i[n])
	