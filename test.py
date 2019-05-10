#!/usr/bin/env python3

from sys import argv, exit as sys_exit
from subprocess import run

input_size = int(argv[1])
memory_limit = int(argv[2])
sample_count = int(argv[3])
repeat = int(argv[4])

for i in range(repeat):
    print(f'running #{i + 1:04} ', end='', flush=True)
    p = run(
        f'./generate.py {input_size} {sample_count} | ./main {memory_limit}',
        capture_output=True, text=True, shell=True
    )
    expected = p.stderr
    actual = p.stdout
    if 'out of memory' in expected:
        print('out of memory')
    elif expected.startswith('<nothing>'):
        print('nothing')
    elif expected == actual:
        print('passed')
    else:
        print('failed')
        print('expected:')
        print(expected)
        print('actual:')
        print(actual)
        sys_exit(1)
