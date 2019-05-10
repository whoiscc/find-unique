# Find Unique - Demo project for PingCAP

[![Build Status](https://travis-ci.com/whoiscc/find-unique.svg?branch=master)](https://travis-ci.com/whoiscc/find-unique)

## File structure

* `main.cpp` find the first unique word from huge input with limited memory
* `generate.py` random text generator based on content of `/usr/shared/dict/words`
* `test.py` integrated test for presentation and CI

## Before start

* Python 3.7
* `pip install -r requirements.txt`
* `c++ -O3 -std=c++11 -o main main.cpp`

## How to use it

```
$ ./main <memory_limit>
```

* Read from standard input and print the first occurred unique word to standard output.
* If there is no unique word, **the result is undefined behavior**.
* `<memory_limit>` should be specified in MiB. If the input cannot be processed with required memory size, an unhandled `OutOfMemoryException` will be thrown.

> Conceptually it is not possible to achieve the goal with arbitrary input. Consider a 100GiB input file with three words, and each word is 33.3GiB. Then at least 66.7GiB memory is required to find out which of them will be duplicated (or neither of them is duplicated). Generally speaking, the total used memory space increases as the entropy of input goes up, so out of memory exception is more likely to happen when the input has more variability.

```
$ ./generate.py <text_size> [<sample_count>] [<unique_word_count>]
```

* Read from words file under `/usr/share`, produce at least `<text_size>` (in MiB) random text to standard output.
* The random text is made up with words from the words file, separated with whitespace.
* If `<sample_count>` is specified, only the number of that of words will be sampled from words file and be used to generate text.
* `<unique_word_count>` controls how many words appears only once in the output text. Default value is 10.

After execution the script print the first unique word to standard error. Notice that there may be no unique word in the output text even with reasonable arguments in consideration of efficiency. In this case `<nothing>` will be print to standard error.

----

Sample usage:

```
$ ./generate.py 100 100 | ./main 16
garbler
garbler
$ ./generate.py 100 100 | ./main 16
<nothing>
homomallous
$ ./generate.py 100 100 | ./main 16
cofferwork
cofferwork
$ ./generate.py 100 100 | ./main 16
furring
furring
$ ./generate.py 100 10000 | ./main 16
curricula
curricula
$ ./generate.py 100 100000 | ./main 16
linoleic
linoleic
$ ./generate.py 100 200000 | ./main 16
libc++abi.dylib: terminating with uncaught exception of type OutOfMemoryException: out of memory
Traceback (most recent call last):
  File "./generate.py", line 37, in <module>
    print(word, end=' ')
BrokenPipeError: [Errno 32] Broken pipe
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
BrokenPipeError: [Errno 32] Broken pipe
[1]    2907 exit 120   ./generate.py 100 200000 |
       2908 abort      ./main 16
```

The first line of output is standard error from `generate.py`, and the last line of standard output from `main`.

```
$ ./test.py <text_size> <memory_limit> <sample_count> <repeat_time>
```

Repeat the command above for `<repeat_time>` times. For each time, output `passed` if the words are matched, output `failed`, `nothing` and `out of memory` in other cases. `nothing` and `out of memory` is considered as passed test result.

To make a demo run with 1/1024 scaled data size as requested in problem:

```
$ ./test.py 100 16 $COUNT $REPEAT
```

The test running on CI is in this size for saving time.

## Roadmap

* Multithreading support.
* Checking for evil input text. Currently the code in `main` assumes words are not ridiculously long.
* More reality tests.
