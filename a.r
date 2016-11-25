library("ggplot2")

# normalizes all values given in vector 'x' to be between 0,1
normalize <- function(x){
  xmin = min(x)
  xmax = max(x)
  y = (x-xmin)/(xmax-xmin)
  return(y)
}

nlm <- function(x, y){
  return(lm(normalize(y)~normalize(x)))
  
}

d<-read.csv("up.3.saved.txt",sep = "\t")

d$w.len <- nchar(as.character(d$phones))
d$pre.len <-nchar(as.character(d$prefix))
d$suf.len <-nchar(as.character(d$suffix))

d$word_given_context = normalize(d$word_info)
d$prefix_given_suffix = normalize(d$prefix_info)
d$suffix_given_prefix = normalize(d$suffix_info)

# because it's based off of index in Python, 0 is first character, etc
d$u.point = d$u.point + 1
#d$word_given_context = log1p(d$word_info)
#d$prefix_given_suffix = log1p(d$prefix_info)
#d$suffix_given_prefix = log1p(d$suffix_info)



mono <- subset(d, morpheme_count == 0)

plot(density(mono$word_given_context))
plot(density(mono$suffix_given_prefix))
plot(density(mono$prefix_given_suffix))

# MORE surprising the word, LESS surprising the prefix
summary(lm(mono$word_given_context ~ mono$prefix_given_suffix))
# MORE surprising the word, MORE surprising the suffix
# NOT signif
summary(lm(mono$word_given_context ~ mono$suffix_given_prefix))

ggplot(mono, aes(prefix_given_suffix, word_given_context)) +
  geom_point() + geom_smooth(method="lm")

ggplot(mono, aes(suffix_given_prefix, word_given_context)) +
  geom_point() + geom_smooth(method="lm")

ggplot(mono, aes(x= word_given_context, y = normalize(u.point/w.len))) +
  geom_smooth(method="lm")
summary(lm(normalize(mono$u.point_mass/mono$u.point) ~ mono$word_given_context))

ggplot(mono, aes(suffix_given_prefix, word_given_context)) + 
  geom_smooth(method="lm")

qplot(mono$word_given_context, mono$prefix_given_suffix)

ggplot(mono, aes(x = normalize(w.len), y = normalize(suffix_info))) +
  geom_point()
summary(lm(mono$suffix_info ~ mono$w.len))

