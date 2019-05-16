#!/bin/bash

set -e

change_word_len() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/\(AVER_WORD_LEN =\) .*/\1 $1/" config.py
  else
    sed -i "s/\(AVER_WORD_LEN =\) .*/\1 $1/" config.py
  fi
}

# short word
change_word_len 10
for i in {1..10}
do
  python gen.py 2> expect.txt | python main.py > real.txt
  diff expect.txt real.txt
done

# long word
change_word_len '1 << 9'
for i in {1..10}
do
  python gen.py 2> expect.txt | python main.py > real.txt
  diff expect.txt real.txt
done
