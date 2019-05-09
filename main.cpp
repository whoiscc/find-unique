#include <iostream>
#include <cstdio>

using namespace std;

size_t fill_buffer(char *buffer, size_t buffer_len) {
  return fread(buffer, sizeof(char), buffer_len, stdin);
}

int main() {
  char buffer[128];
  while (true) {
    size_t len = fill_buffer(buffer, 128);
    cout << len << endl;
    if (len == 0) {
      break;
    }
  }

  return 0;
}
