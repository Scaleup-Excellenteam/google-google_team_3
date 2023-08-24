class TrieNode:

    def __init__(self, char):
        self.char = char
        # keys are characters, values are nodes
        self.children = {}
        # keys are sentence id, values are offsets
        self.sentences_id = {}


class Trie:
    def __init__(self):
        self.root = TrieNode('')  # Initialize the root node

    def insert(self, word, sentence_id, place_in_sentence):
        node = self.root
        word = word.lower()

        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        if sentence_id in node.sentences_id:
            node.sentences_id[sentence_id].append(place_in_sentence)
        else:
            node.sentences_id[sentence_id] = [place_in_sentence]

    def get_sentences_of_word(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                return None
            else:
                node = node.children[char]

        return node.sentences_id

