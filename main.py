#

import sys

from config import *
from find_unique.block_manager import LRUBlockManager
from find_unique.word import iter_words


def main():
    bm = LRUBlockManager(
        sys.stdin, BLOCK_SIZE, CACHED_BLOCK_COUNT, CACHE_DIR,
    )
    word_window = []
    possible_unique = []
    for index, word in enumerate(iter_words(bm)):
        for exist_index, exist_word in enumerate(word_window):
            if possible_unique[exist_index] and exist_word == word:
                possible_unique[exist_index] = False
        word_window.append(word)
        possible_unique.append(True)
        if (index + 1) % WINDOW_SIZE != 0:
            continue
        # print('window full')

        for rest_word in iter_words(bm, word.offset + word.length + 1):
            for window_index, window_word in enumerate(word_window):
                if possible_unique[window_index] and window_word == rest_word:
                    possible_unique[window_index] = False
        for unique, word in zip(possible_unique, word_window):
            if unique:
                for part in word.iter_parts():
                    print(part, end='')
                return
        word_window = []
        possible_unique = []

    # for the last half-filled window
    for unique, word in zip(possible_unique, word_window):
        if unique:
            for part in word.iter_parts():
                print(part, end='')
        return


if __name__ == '__main__':
    main()
    print('')
