#!/usr/bin/env python3

with open('/usr/share/dict/words') as words_file:
    words_list = words_file.read().split('\n')

from sys import argv, stderr

total_length = int(argv[1])
current_length = 0

from numpy.random import choice, randint

sample_count = len(words_list) if len(argv) <= 2 else int(argv[2])
words_list = choice(words_list, size=(1, sample_count), replace=False)
unique_position = {}
current_index = 0
# generate random integers in batch to improve performance
word_indices = randint(sample_count, size=(1, 1024))
while current_length < total_length:
    if current_index == 1024:
        word_indices = randint(sample_count, size=(1, 1024))
        current_index = 0
    word_index = int(word_indices[0, current_index])
    current_index += 1
    if word_index not in unique_position:
        unique_position[word_index] = current_length
    else:
        unique_position[word_index] = total_length  # duplicated

    word = words_list[0, word_index]
    print(word, end=' ')
    current_length += len(word) + 1  # plus 1 for '\n'


word_index, position = min(unique_position.items(), key=lambda pair: pair[1])
if position == total_length:
    print('<Nothing>', file=stderr)
else:
    print(words_list[0, word_index], file=stderr)
