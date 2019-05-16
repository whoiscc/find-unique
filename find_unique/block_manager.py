#

class BlockManager:
    def __init__(self, file, block_size, cache_dir):
        self.input = file
        self.block_size = block_size
        self.unread_index = 0
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)

        self.io_count = 0

    def read_block(self):
        return self.input.read(self.block_size)

    def get_block(self, block_index):
        # cannot skip unread blocks
        assert 0 <= block_index <= self.unread_index
        if block_index == self.unread_index:
            block = self.read_block()
            self.io_count += 1
            with open(
                self.cache_dir / f'block-{self.unread_index}.txt', 'w'
            ) as block_file:
                block_file.write(block)
            self.unread_index += 1
        else:
            self.io_count += 1
            with open(
                self.cache_dir / f'block-{block_index}.txt'
            ) as block_file:
                block = block_file.read()
        return block


class LRUBlockManager(BlockManager):
    def __init__(self, file, block_size, cached_block_count, cache_dir):
        super().__init__(file, block_size, cache_dir)
        self.block_count = cached_block_count
        self.blocks = {}
        self.last_used = {}
        self.time = 0

    def get_block(self, block_index):
        # print(f'get_block: {block_index}')
        if block_index not in self.blocks:
            if len(self.blocks) == self.block_count:
                lru_block_index, _ = min(
                    self.last_used.items(), key=lambda p: p[1])
                del self.blocks[lru_block_index]
                del self.last_used[lru_block_index]
            self.blocks[block_index] = super().get_block(block_index)
        self.last_used[block_index] = self.time
        self.time += 1
        return self.blocks[block_index]
