#

from config import *

from numpy.random import choice, randint
from numpy import argmin

import sys


alphabet = [chr(x) for x in range(ord('a'), ord('z') + 1)]

def next_word(word_length, char_list, char_index):
    word = char_list[char_index:char_index + word_length]
    return ''.join(word), char_index + word_length


def main():
    char_list = choice(alphabet, size=(TEXT_LEN,))
    char_index = 0
    word_len_min = AVER_WORD_LEN - WORD_LEN_HALF_RANGE
    word_len_max = AVER_WORD_LEN + WORD_LEN_HALF_RANGE
    word_len_list = (l for l in randint(
        word_len_min, word_len_max,
        size=(TEXT_LEN // word_len_min,),
    ))

    # choose unique words & position
    unique_words = {}
    unique_words_pos = choice(
        range(TEXT_LEN // word_len_max),
        size=(UNIQUE_WORD_COUNT,), replace=False)
    first_unique_index = argmin(unique_words_pos)
    for i in range(UNIQUE_WORD_COUNT):
        word, char_index = next_word(
            next(word_len_list), char_list, char_index)
        unique_words[word] = unique_words_pos[i]
        if i == first_unique_index:
            print(word, file=sys.stderr)

    # generate
    gen_len = 0
    words = []
    word_count = 0
    while gen_len < TEXT_LEN // 2:
        unique = False
        for word, pos in unique_words.items():
            if word_count == pos:
                print(word, end=WORD_SEP)
                unique = True
                break
        if not unique:
            word, char_index = next_word(
                next(word_len_list), char_list, char_index)
            print(word, end=WORD_SEP)
            words.append(word)
        gen_len += len(word) + 1
        word_count += 1

    for word in words:
        print(word, end=WORD_SEP)


if __name__ == '__main__':
    main()
