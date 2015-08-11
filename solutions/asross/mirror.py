from collections import defaultdict

# get a list of all words
f = open('/usr/share/dict/words', 'r')
words = f.read().lower().split("\n")

# get the alphabet
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# generate a dictionary of { first_letter => { last_letter => [words] } }, given some criteria
def generate_word_dictionary(min_length=2):
    words_by_first_and_last_letter = defaultdict(lambda: defaultdict(list))
    for word in words:
        if len(word) >= min_length:
            words_by_first_and_last_letter[word[0]][word[-1]].append(word)
    return words_by_first_and_last_letter

# given a dictionary, loop through the alphabet and the offset alphabet
# to find a mirror-alphabet word list
def generate_mirror_word_list(words_by_first_and_last_letter):
    for offset in range(len(alphabet)):
        word_list = []
        for i in range(len(alphabet)):
            first_letter = alphabet[i]
            last_letter = alphabet[(i+offset)%len(alphabet)]
            words = words_by_first_and_last_letter[first_letter][last_letter]
            if len(words) == 0: break
            word_list.append(first_letter + ' is for ' + words[0])

        # we succeeded if the word list contains words for every letter
        if len(word_list) == len(alphabet):
            return word_list

# 1
for word in generate_mirror_word_list(generate_word_dictionary()):
    print word
"""
a is for abaissed
b is for baalite
c is for caitiff
d is for dabbling
e is for each
f is for falisci
g is for gaj
h is for hack
i is for iatrical
j is for jackassism
k is for kabardian
l is for lacto
m is for machopolyp
n is for nastaliq
o is for oar
p is for pabulous
q is for quadrant
r is for raghu
s is for sanjeev
t is for tablefellow
u is for ulex
v is for vacancy
w is for waltz
x is for xanthelasma
y is for yagnob
z is for zac
"""

print '-------'

# 2
for word in generate_mirror_word_list(generate_word_dictionary(min_length=4)):
    print word
# almost the same --
"""
a is for abaissed
b is for baalite
c is for caitiff
d is for dabbling
e is for each
f is for falisci
g is for gunj
h is for hack
i is for iatrical
j is for jackassism
k is for kabardian
l is for lacto
m is for machopolyp
n is for nastaliq  <--- this appears to be the word in question: http://en.wikipedia.org/wiki/Nasta%CA%BFl%C4%ABq_script
o is for oatear
p is for pabulous
q is for quadrant
r is for raghu
s is for sanjeev
t is for tablefellow
u is for ulex
v is for vacancy
w is for waltz
x is for xanthelasma
y is for yagnob
z is for zacatec
"""

print '------'

# BONUS
import urllib
import re

# rather than including a giant list in source control, let's just download the list and parse it here
wikipedia_html = urllib.urlopen("http://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/PG/2005/10/1-10000").read()

# the list consists of links that look like: <a href="/wiki/the" title="the">the</a> = 52428551
# get them using regular expressions
words_in_order_of_frequency = re.findall('<a href="\/wiki\/[a-z]*" title="[a-z]*">([a-z]*)<\/a> = [0-9]*', wikipedia_html)

# a couple get thrown out because they contain periods or punctuation
assert(len(words_in_order_of_frequency) > 9000 and len(words_in_order_of_frequency) < 10000)

# make a set of them to do fast lookups
frequent_words_set = set(words_in_order_of_frequency)

# translate this into a sort index that, failing inclusion, also favors shorter words
def frequency_sort_index(w):
    if w in frequent_words_set:
        return words_in_order_of_frequency.index(w)
    else:
        return len(words_in_order_of_frequency)+len(w)

# generate a dictionary but sort the words by frequency/length, so when we grab the first,
# we get the simplest
word_dictionary = generate_word_dictionary()
for letter1 in alphabet:
    for letter2 in alphabet:
        word_dictionary[letter1][letter2] = sorted(word_dictionary[letter1][letter2], key=frequency_sort_index)

# sanity check
assert(word_dictionary['t']['e'][0] == 'the')

for word in generate_mirror_word_list(word_dictionary):
    print word

# and it's actually somewhat simple...
"""
a is for and
b is for be
c is for chief
d is for during
e is for each
f is for fi
g is for gaj
h is for horseback
i is for individual
j is for jam
k is for known
l is for lo
m is for map
n is for nastaliq
o is for or
p is for perhaps
q is for quiet
r is for raku
s is for sov
t is for throw
u is for ulex
v is for very
w is for waltz
x is for xema
y is for yalb
z is for zinc
"""
