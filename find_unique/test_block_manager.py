#

from io import StringIO
from pathlib import Path

import pytest

from .block_manager import *


def test_block_manager(tmp_path):
    input = StringIO("abcdef")
    manager = BlockManager(input, 4, tmp_path / "cache")
    with pytest.raises(Exception):
        manager.get_block(1)
    for i in range(10):
        assert manager.get_block(0) == "abcd"
    for i in range(10):
        assert manager.get_block(1) == "ef"
    for i in range(10):
        assert manager.get_block(0) == "abcd"
    for i in range(10):
        assert manager.get_block(1) == "ef"


def test_lru_block_manager(tmp_path):
    input = StringIO("abcdef")
    manager = LRUBlockManager(input, 4, 2, tmp_path / "cache")
    with pytest.raises(Exception):
        manager.get_block(1)
    for i in range(10):
        assert manager.get_block(0) == "abcd"
    for i in range(10):
        assert manager.get_block(1) == "ef"
    for i in range(10):
        assert manager.get_block(0) == "abcd"
    for i in range(10):
        assert manager.get_block(1) == "ef"
    
    assert manager.io_count < 40

from random import choices

def test_random(tmp_path):
    alphabet = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    string = ''.join(choices(alphabet, k=1024))
    input = StringIO(string)
    manager = LRUBlockManager(input, 4, 16, tmp_path / "cache")
    for i in range(1024 // 4):
        assert manager.get_block(i) == string[i * 4:(i + 1) * 4]
    for i in choices(range(1024 // 4), k=1024):
        assert manager.get_block(i) == string[i * 4:(i + 1) * 4]
