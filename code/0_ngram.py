import re, sys, math

from 1_housekeeping import *

# meat and potatoes

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

def save_informativity_file(infor, outfile = "avg_informativity.txt"):
	"""
	format - word TAB informativity
	"""

	with open(outfile, "w") as wF:
		for i in infor:
			wF.write(i + "\t" + str(infor[i]) + "\n")


if __name__ == "__main__":

	# only do this the first time you run, afterwards,
	# it should run much faster
	should_preprocess = False

	if should_preprocess:
		preprocess_COCA()
		print()
		sys.exit(0)

	# use the first argument as the COCA (or smaller version) to 
	# calc everything
	b = build_ngrams("COCA.clean.txt",2)

	print("Done making n-grams. Saving....")
	save_ngram_file(b)

	print("\n10 most frequent ngrams:")
	for n in sorted(b, key = lambda g: b[g], reverse=True)[:10]:
		print(n,b[n])

	i = ngram_informativity(b)
	print("Done calculating informativity. Saving....")
	save_informativity_file(i)

	print("\n10 most informative words:")
	for n in sorted(i, key = lambda g: i[g], reverse=True)[:10]:
		print("\t", n,i[n])
	
	print("\n10 least informative words:")
	for n in sorted(i, key = lambda g: i[g])[:10]:
		print("\t", n,i[n])
	