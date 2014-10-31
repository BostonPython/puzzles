__author__ = 'Chuck Mock'
from collections import Counter
import re
try: 
    from nltk.corpus import wordnet as wn
    HAVE_WORDNET = True
except:
    HAVE_WORDNET = False

# Set this to True to dump all the combinations and their words.
SHOW_ALL_COMBOS = False

# FUTURE: Fix iteration to handle rotational symmetry.

RINGS = ['BDMJPRSTLN', 'AEIOUYRTLH', 'ACDEORSTLN', 'DHKYRSTLNE']

print "  Solving wordlock puzzle: http://puzzles.bostonpython.com/lock.html"
print "    The lock has 4 rings: " +  "   ".join(RINGS)
print """    Here is what you know about the correct combination:
      The correct combination is a valid English dictionary word.
      The word is also a member of the small set of triple words for this lock, meaning that all 3 words appear on one configuration of the rings.
      These triple words are a time, a chemical, and a food. (And the correct combination word is the food.)
"""
print "  Wait! (loading dictionary /usr/share/dict/words)"
dictwords = {x:1 for x in open('/usr/share/dict/words','r').read().upper().split('\n') if len(x) == 4}
print "    Found {} 4-letter words.".format(len(dictwords))
print

def idx(index, offset):
    return (index + offset) % 10

def word(index, offset):
    (a,b,c,d) = index
    return ''.join([RINGS[0][idx(a, offset)], RINGS[1][idx(b, offset)],
                    RINGS[2][idx(c, offset)],  RINGS[3][idx(d, offset)]])

def words(index):
    return [word(index, offset) for offset in range(10)]

print "  Wait! (checking combinations)"
triplets = set()
counts = Counter()
for index in [(a,b,c,d) for a in range(10) for b in range(10) for c in range(10) for d in range(10)]:
    actual_words = sorted([w.lower() for w in words(index) if w in dictwords])
    count = len(actual_words)
    counts[count] += 1

    if HAVE_WORDNET:
        if count == 3:
            triplets.add(tuple(actual_words))
    else:
        if SHOW_ALL_COMBOS:
            print index, word(index, 0), actual_words

if SHOW_ALL_COMBOS:
    print

print "    There are 10,000 combinations, not adjusting for rotational symmetry."
print "    Distribution of words across the combinations:"
print "        {}   {}".format('Words', 'Combinations')
for wordcount, frequency in sorted(counts.items()):
    print "          {}         {:4d}".format(wordcount, frequency)
print
print "  If you want a listing of all the combinations, edit the code to set SHOW_ALL_COMBOS = True"
print

if not HAVE_WORDNET:
    print "  I can't check the meanings to select the answer right now."
    print "  For meanings, I need something like NLTK and WordNet:"
    print "         http://www.nltk.org"
    print "         http://www.nltk.org/book_1ed/"
    print "         http://wordnet.princeton.edu"
    print
    print """  I'm currently trying to use this code:
         from nltk.corpus import wordnet as wn
         synsets = [synset for synset in wn.synsets(word)]
         definitions = [synset.definition for synset in synsets]
         targets = [definition for definition in definitions if re.search('\Wfood|chemical|time\W', definition)]

  so for example, the word 'code' has these definitions:
       - {}""".format("\n       - ".join([synset.definition for synset in wn.synsets('code')]))

if HAVE_WORDNET:
    print "  Don't tell me!  (finding food, chemical, time)"
    word_definitions = {}
    triplet_scores = []
    for triplet in sorted(triplets):
        triplet_score = 0
        for word in triplet:
            synsets = [synset for synset in wn.synsets(word)]
            definitions = [synset.definition for synset in synsets]
            
            targets = [definition for definition in definitions if re.search('\Wfood|chemical|time\W', definition)]
            if targets:
                word_definition = word_definitions.get(word, None)
                if word_definition is None:
                    if len(targets) == 1:
                        targets = targets[0]
                    word_definitions[word.lower()] = targets
                triplet_score += 1
        triplet_scores.append((triplet_score, triplet))

    triplet_scores.sort()
    triplet_scores.reverse()

    print
    max_score = max([score for score, triplet in triplet_scores])
    answers = [(score,triplet) for score, triplet in triplet_scores if score == max_score]
    if len(answers) > 1:
        print "  Is it one of these?"
    else:
        print "  Is it this one?"

    for score,triplet in answers:
        print "  " + ", ".join(triplet)
        for word in triplet:
            print "     {}:  {}".format(word, word_definitions.get(word, "???"))


print