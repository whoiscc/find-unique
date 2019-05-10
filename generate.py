#!/usr/bin/env python3

with open('/usr/share/dict/words') as words_file:
    words_list = words_file.read().split('\n')

from sys import argv, stderr

total_length = int(argv[1]) * 2 ** 20  # in MB
current_length = 0

from numpy.random import choice, randint

sample_count = len(words_list) if len(argv) <= 2 else int(argv[2])
words_list = choice(words_list, size=(1, sample_count), replace=False)
unique_word_count = 10 if len(argv) <= 3 else int(argv[3])
unique_words_list = words_list[0, :unique_word_count]
unique_position = {word: None for word in unique_words_list}
current_index = 0
# generate random integers in batch to improve performance
randint_batch_size = 2 ** 10
word_indices = randint(sample_count, size=(1, randint_batch_size))
while current_length < total_length:
    # print(current_length)
    if current_index == randint_batch_size:
        word_indices = randint(sample_count, size=(1, randint_batch_size))
        current_index = 0
    word_index = int(word_indices[0, current_index])
    current_index += 1

    word = words_list[0, word_index]
    if word in unique_position:
        if unique_position[word] is not None:
            continue
        else:
            unique_position[word] = current_length

    print(word, end=' ')
    current_length += len(word) + 1  # plus 1 for ' '

# make sure the words in `unique_words_list` are the only unique words
for word in words_list[0, unique_word_count:-1]:
    print(word, end=' ')
print(words_list[0, -1], end='')

# print(unique_position, file=stderr)
word, position = min(
    unique_position.items(),
    key=lambda pair: pair[1] if pair[1] is not None else total_length
)
print(word if position is not None else '<nothing>', file=stderr)
