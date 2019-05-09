#

import os
import psutil
import sys

def remain_memory(total = 16 * 2 ** 30):
    p = psutil.Process(os.getpid())
    return total - p.memory_info().rss

unique_map = {}

DUPLICATED = 16 * 2 ** 30
class Updater:
    def __init__(self):
        self.count = 0

    def update_map(self, unique_map, word):
        # print('word: ', word)
        if word not in unique_map:
            unique_map[word] = self.count
            self.count += 1
        else:
            unique_map[word] = DUPLICATED

updater = Updater()
total_len = 0
half_word = ''
total_memory = 16 * 2 ** 30 if len(sys.argv) <= 1 else int(sys.argv[1]) * 2 ** 20
while True:
    read_size = remain_memory(total_memory) // 2
    # read_size = min(read_size, 4 * 2 ** 30)
    print('read size: ', read_size)
    if read_size <= 0:
        print('No enough memory.', file=sys.stderr)
        sys.exit()
    input_string = sys.stdin.read(read_size)
    if input_string == '':
        break

    input_len = len(input_string)
    # cursor may be -1 if ' ' is not found, which is expected
    cursor = input_string.find(' ')
    word = half_word + input_string[:cursor]
    print('joined word: ', word)
    updater.update_map(unique_map, word)
    while True:
        while cursor < input_len and input_string[cursor] == ' ':
            cursor += 1
        next_cursor = input_string.find(' ', cursor)
        if next_cursor < 0:
            half_word = input_string[cursor:]
            break
        word = input_string[cursor:next_cursor]
        updater.update_map(unique_map, word)
        cursor = next_cursor

if half_word != '':
    updater.update_map(unique_map, half_word)

# print(unique_map)
print(min(unique_map.items(), key=lambda p: p[1])[0])
