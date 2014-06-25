f = open('/usr/share/dict/words', 'r')
words = set(f.read().upper().split("\n"))

prefixes = set([''])
for word in words:
    l = len(word)
    for i in range(l):
        prefixes.add(word[0:l-i])

# NOTE:
# you need a file pi_billion.txt to run this, which I didn't include in git
# for obvious reasons :)

#pi_chars = list(open('./pi.txt').read())[2:]
pi_chars = list(open('./pi_billion.txt').read(int(1e9)))[2:]

word_so_far = ''
index = 0
longest_word = ''
i = 0
while len(longest_word) < 7:
    index = 0
    word_so_far = ''
    while word_so_far in prefixes:
        word_so_far += chr(int(str(pi_chars[i+index])+str(pi_chars[i+index+1])))
        index += 2

        if word_so_far in words:
            if len(word_so_far) > len(longest_word):
                print "NEW WORD: ", word_so_far, i
                longest_word = word_so_far
            elif len(word_so_far) >= 6:
                print "OLD WORD", word_so_far, i

    i += 1

"""
NEW WORD:  A 6
NEW WORD:  YO 10
NEW WORD:  MUM 620
NEW WORD:  MANS 19960
NEW WORD:  MIXEN 883090
NEW WORD:  SCHEMY 8934935
OLD WORD UNEVIL 33952449
OLD WORD LATEST 181824140
OLD WORD SCALMA 183156350
OLD WORD BIRKIE 199440161
OLD WORD FABRIC 316604217
OLD WORD STANZA 323841122
OLD WORD LECHWE 341931840
OLD WORD EDDAIC 444461580
OLD WORD DRYOPE 505868624
OLD WORD STAREE 560038168
OLD WORD POSSUM 567155934
OLD WORD COAXER 569388723
OLD WORD NOZZLE 596769724
OLD WORD INDABA 607477452
OLD WORD THRIVE 717932209
OLD WORD NODDLE 770086664
"""
