import random, string

from random_seq import *

def update_cohort(word, cohort, step):
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
			new_cohort[v] = 1
			found_matches = True
		elif found_matches:
			break
	return new_cohort

def calculate_up(word, cohort):
	"""
	using the update_cohort method, we start at 0 (first char) and
	check each word in our starting cohort to find matches
	we then increase the step and check all of the words that made the
	cut at step 0
	we iterate until there are no words EXCEPT the original, ie it's
	unique
	"""
	up = len(word)-1
	cohort_history = [1 for _ in range(len(word))]
	for i in range(len(word)):
		new_cohort = update_cohort(word, cohort, i)
		cohort_history[i] = len(new_cohort)
		cohort = new_cohort
		if len(new_cohort) == 1:
			up = i
			break
	return up, cohort_history

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
		# we'll pass the transcription to the dictionary
		# so we can use it later...
		lex[w] = (coca_words[w], cmud_words[w])

	return lex

def split_word(word, up):
	"""
	given a uniqueness point, split a word into "prefix" and "suffix"
	"""
	prefix = word[:up]
	suffix = word[up:]
	return (prefix, suffix)

print("Loading the files...")
#lex = build_lex("../sample/2-gram_informativity.txt", "CMUDict_Lemma.txt")
lex = build_lex("../sample/test.txt", "CMUDict_Lemma.txt")

#####

#####

print("Done.")
t_lex = [lex[w][1] for w in lex]
up = {}

print("We got", len(t_lex), "to do.\n")
i = 0
for w in t_lex:
	i+=1
	print(i, "Doing ::", w, end="          \r")
	up[w] = (calculate_up(w, t_lex))
print()

#for w in sorted(up, key = lambda v : up[v]):
wf = open("up.saved.txt", "w")
i = 0
for w in sorted(up):
	i += 1
	split = split_word(w, up[w][0])
	writeString = w + "\t" + str(split) + "\t" +  str(up[w])
	print(i, writeString)
	wf.write(writeString + "\n")
wf.close()

"""
c = "abcd"#efghijlmnopqrstuvwxyz"

gen_random_words("test.txt", c=c, max_length=8, max_per_len = 200, min_per_len = 180)
lexicon = read_random_words("test.txt")
up = {}
print(len(lexicon), "total words.\n")
i = 0
for w in lexicon:
	i+=1
	print(i, "Doing ::", w, end="\r")
	up[w] = (calculate_up(w, lexicon))
print()

#for w in sorted(up, key = lambda v : up[v]):
i = 0
for w in sorted(up):
	i += 1
	print(i, w, up[w])
"""