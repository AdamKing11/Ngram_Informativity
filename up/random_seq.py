"""
Adam King

Quick script to generate random sequences of characters and save/load them
"""


def random_seq(l, c):
	"""
	Generates a random string of length 'l' from characters in 'c'
	"""
	return ''.join(random.choice(c) for _ in range(l))

def gen_random_words(outfile, c = "abcdef", min_length = 2, max_length = 6, \
		min_per_len = 50, max_per_len = 300):
	"""
	Creates and saves a list of random character sequences
	"""
	d = {}
	for l in range(min_length,max_length):
		for i in range(random.randrange(min_per_len,max_per_len)):
			d[random_seq(l, c)] = 1

	with open(outfile, "w") as wF:
		for w in d:
			wF.write(w + "\n")

def read_random_words(infile):
	"""
	Reads in a file of random characters and returns a dictionary of them
	(dictionary instead of list in case we want to "weight" the different words 
	or whatever in the future

	i.e. specify different features for words that we use for further... science
	)
	"""
	d = {}
	with open(infile, "r") as rF:
		for l in rF:
			l = l.rstrip()
			d[l] = 1
	return d
