#!/usr/bin/env python3

with open('/usr/share/dict/words') as words_file:
    words_list = words_file.read().split('\n')

from sys import argv, stderr

total_length = int(argv[1])
current_length = 0

from random import randrange, sample

sample_count = len(words_list) if len(argv) <= 2 else int(argv[2])
words_list = sample(words_list, sample_count)
unique_position = {}
while current_length < total_length:
    word_index = randrange(0, sample_count)
    if word_index not in unique_position:
        unique_position[word_index] = current_length
    else:
        unique_position[word_index] = total_length  # duplicated

    word = words_list[word_index]
    print(word, end=' ')
    current_length += len(word) + 1  # plus 1 for '\n'


word_index, position = min(unique_position.items(), key=lambda pair: pair[1])
if position == total_length:
    print('<Nothing>', file=stderr)
else:
    print(words_list[word_index], file=stderr)
