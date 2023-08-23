import pandas as pd
import os

DATA_DIR = "/Archive1"
CURR_DIR = os.path.dirname(os.path.realpath(__file__))


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
                    self.root.sentences_id[sentence_id] = [place_in_sentence]
                else:
                    self.root.sentences_id[sentence_id].append(place_in_sentence)

    def get_sentences_of_word(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                return None

            else:
                node = node.children[char]

        return node.sentences_id


sentences_df = pd.DataFrame(columns=['ID', 'sentence', 'file_path'])
words_trie = Trie()


def initialize_sentences_dataframe(line: str):
    sentences_df.insert()
    return 1


def initialize_words_trie(line: str, sentence_id: int):
    words = line.split()
    for x in range(len(words)):
        words_trie.insert(words[x], sentence_id, x)


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


def run():
    """
        get the sentences that the word is in

    """
    user_input = input("The system is ready, enter your text: \n")
    match_sentences = {}
    words = user_input.split()

    if len(words) > 2:

        for x in range(len(words)):
            # sentences_that_word_appears is a
            sentences_that_word_appears = words_trie.get_sentences_of_word(words[x])
            if sentences_that_word_appears:
                if x == 0:
                    for k in sentences_that_word_appears.keys():
                        match_sentences[k] = 1

                elif x == 1:
                    for k, v in sentences_that_word_appears.items():
                        if match_sentences.get(k) is None:
                            match_sentences[k] = 1

                        else:
                            match_sentences[k] += 1

                else:
                    for k, v in sentences_that_word_appears.items():
                        if (match_sentences.get(k) is None) or (match_sentences.get(k) < x - 1):
                            match_sentences[k] = None
                        else:
                            match_sentences[k] += 1

        return [key for key, value in match_sentences.items() if value >= len(words) - 1]

    else:
        return []


def main():
    print("Loading files and preparing system")
    initialize_data()
    run()


if __name__ == "__main__":
    main()
