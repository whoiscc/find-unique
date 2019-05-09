#

import os
import psutil
import sys

DEFAULT_MAX_MEMORY_SIZE = 16 * 2 ** 30

def remain_memory(total):
    p = psutil.Process(os.getpid())
    return total - p.memory_info().rss

class Recorder:
    def __init__(self):
        self.count = 0
        # unique_map[<word>] = <sequencial number>
        self.unique_map = {}
        self.duplicated = set()

    def update_map(self, word):
        # print('word: ', word)
        # alternative way is store +Inf for duplicated words
        # benchmark required here
        if word in self.duplicated:
            return
        if word not in self.unique_map:
            self.unique_map[word] = self.count
            self.count += 1
        else:
            del self.unique_map[word]
            self.duplicated.add(word)

recorder = Recorder()
total_len = 0
half_word = ''
total_memory = (
    DEFAULT_MAX_MEMORY_SIZE if len(sys.argv) <= 1
    else int(sys.argv[1]) * 2 ** 20  # command line argument in MB
)
while True:
    # in the worst case, every read word is unique, and all the input except
    # whitespaces must be copied into `recorder`
    # so we must make sure usable memory is at least double than input batch
    # size
    # the factor could change in practice according to input's feature
    read_size = remain_memory(total_memory) // 2
    # read_size = min(read_size, 4 * 2 ** 30)
    # print('read size: ', read_size)
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
    # print('joined word: ', word)
    recorder.update_map(word)
    while True:
        while cursor < input_len and input_string[cursor] == ' ':
            cursor += 1
        next_cursor = input_string.find(' ', cursor)
        if next_cursor < 0:
            half_word = input_string[cursor:]
            break
        word = input_string[cursor:next_cursor]
        recorder.update_map(word)
        cursor = next_cursor

if half_word != '':
    recorder.update_map(half_word)

# print(unique_map)
# input data makes sure that there's at least one unique word
# so there will always be at least one tuple in `unique_map.items()`
print(min(recorder.unique_map.items(), key=lambda p: p[1])[0])
