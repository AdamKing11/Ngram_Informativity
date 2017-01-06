from code.up import *
from code.random_seq import *
from code.ngram import *

unigs = {} # for holding unigram counts - key = phonetic transctiption
up = {}	# for holding the Uniqueness points
word_split = {} # for holding a dict - linking a word to its prefix/suffix split
ortho = {} 	# for holding a link between CMUDict transcription and orthography
ps = {}	# for holding a dictionary of prefix_suff (split at upoint)
sp = {}	# for holding a dictionary of suf_prefix (just like above, but switched)
celex_morphemes = {} 	# for holding the count of morphemes for each word
upoint_mass = {}	# for holding the u-point mass for each word
upoint_hist = {}
morph_count = 0


print("Loading the files...")
lex = build_lex("sample/3-gram_informativity.txt", "CMUDict/CMUDict_Lemma.txt")
unigs = load_unigram_file("sample/unigrams.txt")

print("Done.")
# get a list of the CMUDict forms
unigs = dict((lex[w][1], unigs[w]) for w in lex)
t_lex = [lex[w][1] for w in lex][:2000]
t_lex = dict((w, unigs[w]) for w in t_lex)

print(len(t_lex), "words to do.")

# loop through the words and find the uniqueness points
i = 0
for w in t_lex:
	i+=1
	print(i, "Doing ::", w, end="          \r")
	up[w], history, history_freq = calculate_up(w, t_lex)
	upoint_hist[w] = history_freq
print()

for w in up:
	print(w, up[w], unigs[w], upoint_hist[w])
	pass
