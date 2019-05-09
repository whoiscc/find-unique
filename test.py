#!/usr/bin/env python3

from sys import argv, exit as sys_exit
from subprocess import run

input_size = int(argv[1]) * 2 ** 20
memory_limit = int(argv[2])
repeat = int(argv[3])

for i in range(repeat):
    print(f'running #{i + 1:04} ', end='', flush=True)
    p = run(
        f'./generate.py {input_size} | mprof run python3 main.py {memory_limit * 2 ** 20}',
        capture_output=True, text=True, shell=True
    )
    expected = p.stderr
    actual = p.stdout
    if expected.startswith('<Nothing>'):
        print('passed (nothing)')
    elif any([expected.strip() == line for line in actual.split('\n')]):  # there are lines produced by mprof
        print('passed')
    else:
        print('failed')
        print('expected:')
        print(expected)
        print('actual:')
        print(actual)
        sys_exit(1)

    p = run('cat mprofile_*', capture_output=True, text=True, shell=True)
    max_memory_usage = 0
    for line in p.stdout.split('\n'):
        # print(line)
        if not line.startswith('MEM'):
            continue
        memory_usage = float(line.split(' ')[1])
        max_memory_usage = max(max_memory_usage, memory_usage)
    run('mprof clean', shell=True)
    if max_memory_usage > memory_limit:
        print(f'out of memory (max: {max_memory_usage} limit: {memory_limit})')
        sys_exit(1)
