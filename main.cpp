//

#include <iostream>
#include <iomanip>
#include <cstdlib>
#include <ctime>

using namespace std;

typedef unsigned char Byte;

class TextProducer {
public:
  virtual size_t fill(Byte *buffer, size_t max_length) = 0;
  virtual bool check(Byte *word, size_t length, size_t position) = 0;
  virtual ~TextProducer() {}
};

size_t random_word_length(size_t max) {
  size_t len = rand() % 10 + 1;
  return len > max ? max : len;
}

Byte random_word_content() {
  Byte byte;
  do {
    byte = rand() % 256;
  } while (byte == ' ');
  return byte;
}

class RandomTextProducer : public TextProducer {
private:
  size_t total_length, produced_length;
  Byte unique_word[128];
  size_t word_length, word_position;
  bool passed;
public:
  RandomTextProducer(size_t total_length)
    : total_length(total_length), produced_length(0), passed(false) {}

  virtual bool check(Byte *word, size_t length, size_t position) {
    if (!passed) {
      return false;
    }
    if (length != word_length) {
      return false;
    }
    for (size_t i = 0; i < word_length; i++) {
      if (word[i] != unique_word[i]) {
        return false;
      }
    }
    return true;
  }

  virtual size_t fill(Byte *buffer, size_t max_length) {
    size_t length = 0;
    while (length < max_length && produced_length < total_length) {
      size_t max_word_length = max_length - length;
      size_t remain_length = total_length - produced_length;
      max_word_length = max_word_length > remain_length ? remain_length : max_word_length;
      size_t word_length = random_word_length(max_word_length);
      for (size_t i = 0; i < word_length; i++) {
        buffer[i] = random_word_content();
      }
      buffer += word_length;
      length += word_length;
      produced_length += word_length;
      if (length < max_length && produced_length < total_length) {
        *buffer = ' ';
        length += 1;
        produced_length += 1;
      }
    }
    return length;
  }
};


int main() {
  srand(time(NULL));

  TextProducer *producer = new RandomTextProducer(128);

  Byte buffer[128];
  producer->fill(buffer, 128);

  for (size_t i = 0; i < 128; i++) {
    cout << hex << setfill('0') << setw(2) << unsigned(buffer[i]) << " ";
    if (buffer[i] == ' ') {
      cout << endl;
    }
  }
  cout << endl;

  delete producer;

  return 0;
}
