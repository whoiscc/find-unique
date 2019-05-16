# Find Unique - Demo project for PingCAP

[![Build Status](https://travis-ci.com/whoiscc/find-unique.svg?branch=master)](https://travis-ci.com/whoiscc/find-unique)

## File structure

* `main.py` find the first unique word from huge input with limited memory
* `find_unique` supporting library for `main.py`
* `gen.py` random text generator
* `test.sh` integrated test for presentation and CI
* `config.py` configure file used by `gen.py` and `main.py`

## Before start

* Python 3.7
* `pip install numpy`

## How to use it

```
$ python gen.py | python main.py
xsixlxxjl
xsixlxxjl
```

The first line is the standard error of `gen.py`, and the last line is the standard output of `main.py`

## How does it work

`gen.py` generates text with random words. The words are made up with lower case letters and separated by whitespace. The separator, average word length and word length range could be set in `config.py`.

`main.py` read input by blocks. It will cache recently used blocks in memory and store the other read blocks on the disk, like a L1 cache of CPU. To exploit spatial locality, it fills a word window with adjacent words, and compares the following words with all the words in the window. You can also set window size, block size and the number of cached blocks in `config.py`. There's no explicit way to limit the memory used by `main.py`, but it will be constant, approximately block size multiplied by block number plus window size multiplied by the size of `Word` instance.

## Roadmap

* Limit the memory explicitly
* Exploit more spatial locality addition to word window
* Add unit test to `BlockManager` and `Word`
* Variable block size to fix word boundary when possible
* More efficient way to compare words
