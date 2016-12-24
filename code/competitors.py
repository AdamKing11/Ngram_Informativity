"""
go through the n-gram files and for each word, find a list of words that are 
"competitors"
that is, that share the same "contexts" (earlier words in n-gram)

1. get list of all Contexts for each Word
	and all Words for each Context
2. for each word, loop through all contexts
	and add each word from the contexts to a
	set
"""


if __name__ == "__main__":
	word_to_context = {}
	context_to_word = {}
	print("loading ngrams...\n19200000")
	with open("sample/3-grams.txt", "r") as rf:
		i = 0
		for l in rf:
			i += 1
			if i % 15000 == 0:
				print(i, end="\r")
			#if i > 10000:
			#	break
			l = l.rstrip()
			l = l.rsplit("\t")
			l = l[0].rsplit(" ")
			word = l[-1]
			context = tuple(l[:-1])
			
			if word not in word_to_context:
				word_to_context[word] = set([])
			if context not in context_to_word:
				context_to_word[context] = set([])
			word_to_context[word].add(context)
			context_to_word[context].add(word)
	print()
	print("done.\n")
	
	print(len(word_to_context))
	word_to_competitors = {}
	i = 0
	for w in word_to_context:
		i += 1
		if i % 100 == 0:
				print(i, end="\r")
		word_to_competitors[w] = set([])
		for c in word_to_context[w]:
			word_to_competitors[w] = word_to_competitors[w].union(context_to_word[c])
		# for memory efficiency	
			del context_to_word[c]
		del word_to_context[w]

	print()
	print("saving...")
	with open("sample/competitors.txt", "w") as wf:
		for w in word_to_competitors:
			wf.write(w)
			for c in word_to_competitors[w]:
				wf.write("\t" + c)
			wf.write("\n")