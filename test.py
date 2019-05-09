#!/usr/bin/env python3

from sys import argv, exit as sys_exit
from subprocess import run

input_size = int(argv[1]) * 2 ** 20
memory_limit = int(argv[2]) * 2 ** 20
repeat = int(argv[3])

for i in range(repeat):
    print(f'running #{i + 1:04} ', end='', flush=True)
    p = run(
        f'./generate.py {input_size} | python3 main.py {memory_limit}',
        capture_output=True, text=True, shell=True
    )
    expected = p.stderr
    actual = p.stdout
    if expected.startswith('<Nothing>') or actual == expected:
        print('passed')
    else:
        print('failed')
        print('expected:')
        print(expected)
        print('actual:')
        print(actual)
        sys_exit(1)
