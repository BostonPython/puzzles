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


riddle = [56,38,44,56,29]
answer = ''

with open('/usr/share/dict/words') as w:
    words = w.readlines()


def get_mappings(poem):
    poem_set = ''.join(set(poem))
    mapping = {}

    for char in poem_set:
        count = poem.count(char)
        if count in mapping:
            print "Duplicate count of {0} for character {1}".format(count, char)
            mapping[count] = None
        else:
            mapping[count] = char

    for count, char in mapping.items():
        if char == None:
            del mapping[count]


    mapping_reverse = {v:k for k, v in mapping.items()}

    return mapping, mapping_reverse


def solve(mapping, riddle):
    answer = ''
    for num in riddle:
        answer += mapping[num]
    return answer


mapping, mapping_reverse = get_mappings(poem)
answer = solve(mapping, riddle)

print "Mapping: ", mapping

print "Riddle solution: ", answer

riddles = []

for word in words:
    valid = True
    riddle = []
    for letter in word:
        if letter in mapping_reverse:
            riddle.append(mapping_reverse[letter])
        else:
            valid = False
            break
    if valid:
        riddles.append(riddle)


print "Riddles: ", riddles

longest = max(riddles)

print "Longest riddle: ", longest
print "Longest riddle solution: ", solve(mapping, longest)