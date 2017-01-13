import random, string

from code.random_seq import *

def update_cohort(word, cohort, step, with_freq = True):
	"""
	semi-recursive implementation of cohort calculation
	basically, we get a cohort in, we check to see if our
	current word "matches" a cohort member at a particular segment
	and if not, we toss it out of the cohort
	we then return the new cohort and increase the step and go again
	"""
	new_cohort = {}
	found_matches = False
	for v in sorted(cohort):
		if len(v) <= step:
			continue
		if word[step] == v[step]:
			if type(cohort) == dict and with_freq:
				new_cohort[v] = cohort[v]
			else:
				new_cohort[v] = 1
			found_matches = True
		elif found_matches:
			break
	return new_cohort

def calculate_up(word, cohort, with_freq = True):
	"""
	using the update_cohort method, we start at 0 (first char) and
	check each word in our starting cohort to find matches
	we then increase the step and check all of the words that made the
	cut at step 0
	we iterate until there are no words EXCEPT the original, ie it's
	unique
	'with_freq' argument to specify if we want to include WORD FREQUENCY
	when calculating the competitors at each segment position
	"""
	up = len(word)-1
	cohort_history = [1 for _ in range(len(word))]
	cohort_hist_freq = [0 for _ in range(len(word))]
	for i in range(len(word)):
		new_cohort = update_cohort(word, cohort, i)
		cohort_history[i] = len(new_cohort)
		for cw in new_cohort:
			cohort_hist_freq[i] += new_cohort[cw]
		cohort = new_cohort
		if len(new_cohort) == 1:
			up = i
			break
	return up, cohort_history, cohort_hist_freq

def build_lex(COCA_info, CMUDict):
	"""
	goes into an N-gram informativity file (made by the other script) 
	and the CMUDict and gets a list of all words in the N-gram file 
	with corresponding CMUDict transcriptions
	"""

	coca_words = {}
	cmud_words = {}
	lex = {}

	# first, we open up the ngram informativity files...
	with open(COCA_info, "r") as rF:
		for line in rF:
			line = line.rstrip().rsplit("\t")
			if len(line) < 1:
				continue
			coca_words[line[0]] = line[1]
			
	with open(CMUDict, "r") as rF:
		for line in rF:
			line = line.rstrip().rsplit("\t")
			if len(line) < 1:
				continue
			# format of CMUD is orthograph \t transcription \t .....
			# save the transcription with key as orthography
			cmud_words[line[0]] = line[1]

	# now, we want the INTERSECTION of the COCA and CMUD words...
	for w in set(coca_words).intersection(set(cmud_words)):
		# we'll pass the informativity and transcription to the dictionary
		# so we can use it later...
		lex[w] = (coca_words[w], cmud_words[w])

	return lex

def split_word(word, up, up_in_prefix = 0, up_in_suffix = 0):
	"""
	given a uniqueness point, split a word into "prefix" and "suffix"

	"""
	prefix = word[:up]
	suffix = word[up:]
	return (prefix, suffix)

