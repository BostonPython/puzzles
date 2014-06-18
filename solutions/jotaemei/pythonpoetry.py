# M. Page-Lieberman
# 3-June-2014
# python 3.3.1
# OS X 10.6.8
#
# Answers for http://puzzles.bostonpython.com/poetry.html

import re
import string

poem = '''a narrow fellow in the grass
occasionally rides;
you may have met him, did you not,
his notice sudden is.

the grass divides as with a comb,
a spotted shaft is seen;
and then it closes at your feet
and opens further on.

he likes a boggy acre,
a floor too cool for corn.
yet when a child, and barefoot,
i more than once, at morn,

have passed, i thought, a whip-lash
unbraiding in the sun,
when, stooping to secure it,
it wrinkled, and was gone.

several of nature's people
i know, and they know me;
i feel for them a transport
of cordiality;

but never met this fellow,
attended or alone,
without a tighter breathing,
and zero at the bone.'''

coded_phrase = [56,38,44,56,29]

def one():
    return say(coded_phrase)

def say(encoded_phrase):
    histogram = {c: poem.count(c) for c in string.ascii_lowercase}

    # Note: Multiple letters have the same frequency count.
    # Fortunately, the letters in the encoded phrase have unique counts.
    code_map = {v:k for k, v in histogram.items() if v in encoded_phrase}

    # Create word by grabbing the letters in order of the code
    return ''.join([code_map[k] for k in encoded_phrase])

def three(minword, available_letters):
    largest_words = [minword]
    maxlen = len(largest_words[0])

    # prohib should equal 'jqx'
    prohib = ''.join(set(string.ascii_lowercase) - set(available_letters))

    # Old style string replacement as it's seemingly not possible to replace
    #   curly brackets with a trailing comma within a set of outer brackets
    pattern = re.compile('^[^%s]{%s,}$' % (prohib, maxlen), re.IGNORECASE)

    with open('/usr/share/dict/words', encoding='utf-8') as words:
        for line in words:
            if pattern.search(line):
                line = line.rstrip()
                lenline = len(line)
                if lenline is maxlen:
                    largest_words.append(line)
                if lenline > maxlen:
                    largest_words = [line]
                    maxlen = lenline

    return maxlen, largest_words

def two():
    mapped_letters = tuple((c, poem.count(c)) for c in string.ascii_lowercase)
    available_letters = tuple(c for c in string.ascii_lowercase if
    poem.count(c))

    return mapped_letters, available_letters

if __name__ == '__main__':
    print('Python Puzzle: Python Poetry\n')
    answer1 = one()
    print('1) The answer for code {} is "{}".\n'.format(coded_phrase, answer1))
    mapped_letters, available_letters = two()
    print('2) The mapped codes for all letters are {}.\nThe available letters'
        ' are {}.\n'.format(mapped_letters, available_letters))
    counts, words = three(answer1, available_letters)
    print('3) The largest words that can be used to open the door span for'
        ' {} letters.\nThey are {}.'.format(counts, words))