import random, string

from random_seq import *

def update_cohort(word, cohort, step):
	"""
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
	"""
	up = len(word)
	for i in range(len(word)):
		new_cohort = update_cohort(word, cohort, i)
		dif = len(cohort) - len(new_cohort)
		if len(new_cohort) == 1:
			up = i
			break
	return up



c = "abcdefghijlmnopqrstuvwxyz"

gen_random_words("test.txt", c=c, max_length=15, max_per_len = 1000, min_per_len = 400)
lexicon = read_random_words("test.txt")
up = {}
print(len(lexicon), "total words.\n")
i = 0
for w in lexicon:
	i+=1
	print(i, "Doing ::", w, end="\r")
	up[w] = calculate_up(w, lexicon)

#for w in sorted(up, key = lambda v : up[v]):
for w in sorted(w):
	print(w, up[w])
