#

class Word:
    def __init__(self, block_manager, offset, length):
        self.manager = block_manager
        self.offset = offset
        self.length = length

    def iter_parts(self):
        full_block_size = self.manager.block_size
        block_index = self.offset // full_block_size
        block_offset = self.offset % full_block_size
        remain_length = self.length
        while remain_length > 0:
            block = self.manager.get_block(block_index)
            # TODO: prevent string copy
            yield block[block_offset:block_offset + remain_length]
            remain_length -= len(block) - block_offset
            block_index += 1
            block_offset = 0

    def __eq__(self, other):
        if self.length != other.length:
            return False
        total_length = self.length

        iter_a = self.iter_parts()
        iter_b = other.iter_parts()
        block_a = next(iter_a)
        block_b = next(iter_b)
        index_a = index_b = 0
        index = 0
        while index < total_length:
            if block_a[index_a] != block_b[index_b]:
                return False
            index += 1
            if index == total_length:
                continue
            index_a += 1
            index_b += 1
            if index_a == len(block_a):
                block_a = next(iter_a)
                index_a = 0
            if index_b == len(block_b):
                block_b = next(iter_b)
                index_b = 0
        return True


def iter_words(block_manager, begin_index=0):
    full_block_size = block_manager.block_size
    def iter_blocks():
        index = begin_index // full_block_size
        while True:
            block = block_manager.get_block(index)
            if block == '':
                return
            else:
                yield block
                index += 1

    global_index = begin_index
    local_index = begin_index % full_block_size
    blocks = iter_blocks()
    block = next(blocks)
    block_len = len(block)
    # iteration per word
    while True:
        def find_next(space=True):
            nonlocal local_index, global_index, block, block_len
            while block[local_index].isspace() != space:
                local_index += 1
                global_index += 1
                if local_index == block_len:
                    block = next(blocks)
                    block_len = len(block)
                    local_index = 0

        try:
            find_next(space=False)
        except StopIteration:
            return
        word_start = global_index

        try:
            find_next(space=True)
        except StopIteration:
            pass
        word_end = global_index

        yield Word(block_manager, word_start, word_end - word_start)
