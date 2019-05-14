#

from config import *

from numpy.random import choice, randint
import sys


alphabet = [chr(x) for x in range(ord('a'), ord('z') + 1)]

def random_word(len_list, len_index, char_list, char_index):
    word_len = len_list[0, len_index]
    word = char_list[0, char_index:char_index + word_len]
    # print(word)
    return ''.join(word), len_index + 1, char_index + word_len


def main():
    char_list = choice(alphabet, size=(1, TEXT_LENGTH // 2))
    len_list = randint(
        AVER_WORD_LENGTH - WORD_LENGTH_HALF_RANGE, 
        AVER_WORD_LENGTH + WORD_LENGTH_HALF_RANGE,
        size=(1, TEXT_LENGTH // (AVER_WORD_LENGTH - WORD_LENGTH_HALF_RANGE) + 1))
    char_index = 0
    len_index = 0
    word_dict = set()
    unique_words = {}
    unique_words_pos = choice(
        TEXT_LENGTH // (AVER_WORD_LENGTH + WORD_LENGTH_HALF_RANGE),
        size=(1, UNIQUE_WORD_COUNT), replace=False)
    for i in range(UNIQUE_WORD_COUNT):
        word, len_index, char_index = random_word(
            len_list, len_index, char_list, char_index)
        unique_words[word] = unique_words_pos[0, i]
    
    word_count = 0
    first_unique = None
    text_size = 0
    while text_size < TEXT_LENGTH // 2:
        unique = False
        for word, pos in unique_words.items():
            if pos == word_count:
                print(word, end=' ')
                if first_unique is None:
                    first_unique = word
                unique = True
                break
        if not unique:
            word, len_index, char_index = random_word(
                len_list, len_index, char_list, char_index)
            word_dict.add(word)
            print(word, end=' ')
        text_size += len(word)
        word_count += 1

    assert(first_unique is not None)
    print(first_unique, file=sys.stderr)

    for word in word_dict:
        print(word, end=' ')


main()
