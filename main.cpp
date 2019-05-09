//

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <exception>

using namespace std;

const size_t DUPLICATED = SIZE_MAX;
const size_t NO_OCCURRENCE = SIZE_MAX - 1;

const size_t NOT_APPLICABLE = SIZE_MAX;

struct LetterNode {
  char letter;
  // If there is no word ending on this node, then `NO_OCCURRENCE`.
  // If there is a duplicated word then `DUPLICATED`.
  // If there is a unique word ending here, then `position` becomes a sequential
  // number ralative to other unique words. The word appears first in the input
  // text gets least `position`.
  size_t position;
  // "abc" -> "abd" if nodes[next_letter].letter = 'd'
  // if there's no more replacement for last letter then `NOT_APPLICABLE`
  size_t next_letter;
  // "abc" -> "abcd" if nodes[next_layer].letter = 'd'
  // if there's no more postfix then `NOT_APPLICABLE`
  size_t next_layer;
};

// In the worst case, we need to store a LetterNode instance for every char
// of input.
const size_t INPUT_RATIO = sizeof(LetterNode) / sizeof(char);

struct OutOfMemoryException : public exception {
  virtual const char *what() const noexcept {
    return "out of memory";
  }
};

struct WordTree {
  LetterNode *nodes;
  // implicit root at 0
  size_t next_available;
  size_t seq;
  size_t limit;

  WordTree(size_t nodes_size_limit)
    // allocating whole memory block needed by `nodes` here to prevent copying
    // caused by `realloc`
    // this works well on macOS, since it only allocates memory page when it
    // is actually written
    // cross platform surpporting may be added
    : nodes(new LetterNode[nodes_size_limit]), next_available(0), seq(0),
      limit(nodes_size_limit) {}

  // find the index if `LetterNode` in `nodes`, which represents `word[:len]`
  size_t find_node_index(char *word, size_t len) {
    return find_node_index_impl(
      word, len, 0, next_available == 0 ? NOT_APPLICABLE : 0
    );
  }

  size_t find_node_index_impl(
    char *word, size_t len, size_t current_index, size_t current_node
  ) {
    if (current_node == NOT_APPLICABLE) {
      if (next_available == limit) {
        throw OutOfMemoryException();
      }
      current_node = next_available;
      next_available += 1;

      nodes[current_node].letter = word[current_index];
      nodes[current_node].next_letter = NOT_APPLICABLE;
      nodes[current_node].position = NO_OCCURRENCE;

      if (current_index == len - 1) {
        nodes[current_node].next_layer = NOT_APPLICABLE;
        return current_node;
      } else {
        // `next_available` will become the index of corresponding node since
        // `current_node` argument is `NOT_APPLICABLE`, or exception happens
        // set `next_layer` first to prevent backward reference and save memory
        // same below
        nodes[current_node].next_layer = next_available;
        return find_node_index_impl(
          word, len, current_index + 1, NOT_APPLICABLE
        );
      }
    } else {
      char current_letter = nodes[current_node].letter;
      if (current_letter == word[current_index]) {
        if (current_index == len - 1) {
          return current_node;
        } else {
          size_t next_layer = nodes[current_node].next_layer;
          if (next_layer == NOT_APPLICABLE) {
            nodes[current_node].next_layer = next_available;
          }
          return find_node_index_impl(word, len, current_index + 1, next_layer);
        }
      } else {
        size_t next_letter = nodes[current_node].next_letter;
        if (next_letter == NOT_APPLICABLE) {
          nodes[current_node].next_letter = next_available;
        }
        return find_node_index_impl(word, len, current_index, next_letter);
      }
    }
  }

  void update_node(char *word, size_t len) {
    size_t node_index = find_node_index(word, len);
    size_t position = nodes[node_index].position;
    if (position == NO_OCCURRENCE) {
      nodes[node_index].position = seq;
      seq += 1;
    } else {
      // no matter it was unique or duplicated already
      nodes[node_index].position = DUPLICATED;
    }
  }

  void find_first_unique(char *result_buffer, size_t len) {
    char *temp_buf = new char[len];
    find_first_unique_impl(result_buffer, len, temp_buf, 0, 0, DUPLICATED);
    delete[] temp_buf;
  }

  size_t find_first_unique_impl(
    char *result, size_t len, char *buf, size_t buf_index, size_t current_node,
    size_t min_position
  ) {
    // `buf[:buf_index + 1]` always equals to the word represented by current
    // node
    buf[buf_index] = nodes[current_node].letter;
    size_t position = nodes[current_node].position;
    if (position < min_position) {
      min_position = position;
      strncpy(result, buf, buf_index + 1);
      result[buf_index + 1] = '\0';
    }
    size_t next_layer = nodes[current_node].next_layer;
    if (next_layer != NOT_APPLICABLE) {
      min_position = find_first_unique_impl(
        result, len, buf, buf_index + 1, next_layer, min_position
      );
    }
    size_t next_letter = nodes[current_node].next_letter;
    if (next_letter != NOT_APPLICABLE) {
      min_position = find_first_unique_impl(
        result, len, buf, buf_index, next_letter, min_position
      );
    }
    return min_position;
  }
};

size_t next_word(char *buffer, size_t len, size_t begin) {
  size_t i;
  for (i = begin; i < len && buffer[i] != ' '; i += 1)
    ;
  return i;
}

int main(int argc, char *argv[]) {
  size_t memory_limit;
  if (argc >= 2) {
    sscanf(argv[1], "%zu", &memory_limit);
  } else {
    cerr << "please specify memory limit (in MB)" << endl;
    exit(1);
  }
  size_t nodes_size_limit = (memory_limit << 20) / sizeof(LetterNode);
  // cout << "nodes_size_limit: " << nodes_size_limit << endl;
  WordTree tree(nodes_size_limit);

  char buffer[128];
  fread(buffer, sizeof(char), 128, stdin);
  size_t begin = 0;
  while (begin < 128) {
    size_t end = next_word(buffer, 128, begin);
    size_t node_index = tree.find_node_index(buffer + begin, end - begin);
    tree.update_node(buffer + begin, end - begin);
    begin = end + 1;
  }
  tree.find_first_unique(buffer, 128);
  cout << buffer << endl;

  return 0;
}
