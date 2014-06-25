f = open('/usr/share/dict/words', 'r')
words = f.read().lower().split("\n")

hex_words = [[len(word), word]
                for word in words
                  if all(chars in set('abcdef') for chars in word)]

print max(hex_words)
