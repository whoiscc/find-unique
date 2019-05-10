//

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <exception>
#include <cstring>

using namespace std;

const size_t DUPLICATED = SIZE_MAX;
const size_t NO_OCCURRENCE = SIZE_MAX - 1;

const size_t NOT_APPLICABLE = SIZE_MAX;

// assume memory block size is 4KB
const size_t BLOCK_SIZE = 4 << 10;

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
      // printf("%.*s %zu\n", int(len), word, seq);
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
    // plus 1 for '\0' in result
    if (buf_index + 1 >= len) {
      // TODO: dedicated exception
      throw OutOfMemoryException();
    }
    // `buf[:buf_index + 1]` always equals to the word represented by current
    // node
    buf[buf_index] = nodes[current_node].letter;
    // printf("%.*s\n", int(buf_index + 1), buf);
    size_t position = nodes[current_node].position;
    if (position < min_position) {
      min_position = position;
      strncpy(result, buf, buf_index + 1);
      result[buf_index + 1] = '\0';
      // cout << min_position << " " << result << endl;
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



struct Reader {
  char *buffer;
  size_t buffer_len;
  // the word splited by block reading
  char *half_word;
  size_t half_word_len;
  char *joined_word;
  // buffer[cursor:] is not covered by `tree` yet
  size_t cursor;
  size_t memory_limit;
  WordTree &tree;

  Reader(WordTree &word_tree, size_t memory_limit)
    : tree(word_tree), memory_limit(memory_limit), buffer_len(0), cursor(0),
      joined_word(nullptr) {}

  // discard current buffer, read the next part of input into buffer with proper
  // size
  // half_word should be copied out of current buffer before calling
  void read_block() {
    size_t tree_node_count = tree.next_available;
    size_t tree_size = tree_node_count * sizeof(WordTree);
    if (tree_size != 0) {
      tree_size = ((tree_size - 1) / BLOCK_SIZE + 1) * BLOCK_SIZE;
    }
    // TODO: check for very long half_word
    if (memory_limit <= tree_size) {
      throw OutOfMemoryException();
    }
    size_t next_buffer_len = (memory_limit - tree_size) / INPUT_RATIO;
    if (next_buffer_len == 0) {
      throw OutOfMemoryException();
    }

    if (buffer_len != 0) {
      delete[] buffer;
    }
    buffer = new char[next_buffer_len];
    buffer_len = fread(buffer, sizeof(char), next_buffer_len, stdin);
    // end of input, cleanup
    if (buffer_len == 0) {
      delete[] buffer;
    }
    cursor = 0;
  }

  bool next_word(char **out_word, size_t *out_word_len) {
    // free used joined_word
    if (joined_word != nullptr) {
      delete[] joined_word;
    }

    for (; cursor < buffer_len && buffer[cursor] == ' '; cursor += 1)
      ;
    size_t word_len;
    for (
      word_len = 0;
      cursor + word_len < buffer_len && buffer[cursor + word_len] != ' ';
      word_len += 1
    )
      ;

    if (cursor + word_len < buffer_len) {
      // current buffer is not exhuasted
      // word_len must > 0, because buffer[cursor + word_len] == ' '
      // and cursor < buffer_len (or this condition will not hold) so
      // buffer[cursor] != ' ', so buffer[cursor] != buffer[cursor + word_len]
      *out_word = buffer + cursor;
      *out_word_len = word_len;
      cursor += word_len;
      return true;
    } else {
      // current buffer is exhuasted, we need another read
      // cout << "buffer exhuasted" << endl;
      half_word_len = word_len;
      if (half_word_len != 0) {
        half_word = new char[half_word_len];
        strncpy(half_word, buffer + cursor, half_word_len);
      }

      read_block();
      if (buffer_len == 0) {
        // there's nothing to read, half_word (if exists) becomes the last word
        if (half_word_len == 0) {
          return false;
        }
        *out_word = half_word;
        *out_word_len = half_word_len;
        // TODO: refine the interface to notify caller "this is the last word"
        // to reduce the last reading IO
        return true;
      }

      // cover the rest part of the word
      size_t rest_len;
      for (rest_len = 0; rest_len < buffer_len && buffer[rest_len] != ' '; rest_len += 1)
        ;
      if (half_word_len == 0 && rest_len == 0) {
        // whitespace on both sides, simple ignore them and try again
        cursor = rest_len;
        return next_word(out_word, out_word_len);
      }
      // TODO: check very long rest part
      char *joined_word = new char[half_word_len + rest_len];
      if (half_word_len != 0) {
        strncpy(joined_word, half_word, half_word_len);
        delete[] half_word;
      }
      strncpy(joined_word + half_word_len, buffer, rest_len);
      // printf("joined: %.*s\n", int(half_word_len + rest_len), joined_word);
      *out_word = joined_word;
      *out_word_len = half_word_len + rest_len;
      cursor = rest_len;
      return true;
    }
  }
};


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
  Reader reader(tree, memory_limit << 20);

  char *buf;
  size_t buf_len;
  while (reader.next_word(&buf, &buf_len)) {
    tree.update_node(buf, buf_len);
  }
  char result[64];
  tree.find_first_unique(result, sizeof(result) / sizeof(char));
  cout << result << endl;

  return 0;
}
