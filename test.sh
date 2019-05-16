#!/bin/bash

set -e

# short word
sed -i '' 's/\(AVER_WORD_LEN =\) [0-9]*/\1 10/' config.py
for i in {1..10}
do
  python gen.py 2> expect.txt | python main.py > real.txt
  diff expect.txt real.txt
done

# long word
sed -i '' 's/\(AVER_WORD_LEN =\) [0-9]*/\1 1 << 9/' config.py
for i in {1..10}
do
  python gen.py 2> expect.txt | python main.py > real.txt
  diff expect.txt real.txt
done
