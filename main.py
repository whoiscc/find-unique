#

import sys

from config import *
from find_unique.block_manager import LRUBlockManager
from find_unique.word import Word

from random import randrange

def main():
    bm = LRUBlockManager(sys.stdin, BLOCK_SIZE, CACHED_BLOCK_COUNT)
    first_word = Word(bm, 0, 2)
    for i, part in enumerate(first_word.iter_parts()):
        print(i, part)
    print(first_word == Word(bm, 7, 2))

if __name__ == '__main__':
    main()
