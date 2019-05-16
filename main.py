#

import sys

from config import *
from find_unique.block_manager import LRUBlockManager
from find_unique.word import iter_words

from random import randrange

def main():
    bm = LRUBlockManager(
        sys.stdin, BLOCK_SIZE, CACHED_BLOCK_COUNT, CACHE_DIR,
    )
    for word in iter_words(bm):
        unique = True
        # TODO: iterate following words only
        for another_word in iter_words(bm, word.offset + word.length + 1):
            if word == another_word:
                unique = False
                break
        if unique:
            for part in word.iter_parts():
                print(part, end='')
            break

if __name__ == '__main__':
    main()
