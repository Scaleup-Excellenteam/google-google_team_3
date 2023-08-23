import pandas as pd
import os


class TrieNode:

    def __init__(self, char):
        self.char = char

        # keys are characters, values are nodes
        self.children = {}

        # keys are sentence id, values are offsets
        self.sentences_id = {}


class Trie:

    def __init__(self):
        self.root = TrieNode("")

    def insert(self, word, sentence_id, place_in_sentence):

        node = self.root

        for x in range(len(word)):
            if word[x] in node.children:
                node = node.children

            else:
                new_node = TrieNode(word[x])
                node.children[word[x]] = new_node
                node = new_node

            if x == len(word) - 1:
                if self.root.sentences_id.get(sentence_id) is None:
                    self.root.sentences_id[sentence_id] = place_in_sentence


DATA_DIR = "/Archive"
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
sentences_df = pd.DataFrame(columns=['ID', 'sentence', 'file_path'])
words_trie = Trie()


def initialize_sentences_dataframe(line: str):
    sentences_df.insert()
    return 1



def initialize_words_trie(line: str, sentence_id: int):
    words = line.split()
    for x in range(len(words)):
        words_trie.insert(words[x], sentence_id, x)
    for word in words:
        words_trie.insert(word, sentence_id)



def initialize_data():
    directory = CURR_DIR + DATA_DIR

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(subdir, file))
            if file.endswith('.txt'):
                with open(os.path.join(subdir, file)) as txt_file:
                    for line in txt_file:
                        sentence_id = initialize_sentences_dataframe(line)
                        initialize_words_trie(line, sentence_id)


def main():
    initialize_data()


if __name__ == "__main__":
    main()
