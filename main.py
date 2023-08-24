import pandas as pd
import os
from Trie import Trie

DATA_DIR = "/Archive1"
CURR_DIR = os.path.dirname(os.path.realpath(__file__))


def initialize_sentences_dataframe(line: str, path: str):
    sentences_df.loc[len(sentences_df)] = [line, path]
    return len(sentences_df)


def initialize_words_trie(line: str, sentence_id: int):
    words = line.split()
    for x in range(len(words)):
        words_trie.insert(words[x], sentence_id, x)


def contains_words(line):
    return any(c.isalpha() for c in line)


def initialize_data():
    directory = CURR_DIR + DATA_DIR

    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(subdir, file)) as txt_file:
                    for line in txt_file:
                        line = line.strip()
                        if contains_words(line):
                            sentence_id = initialize_sentences_dataframe(line, file)
                            initialize_words_trie(line, sentence_id)


def run():
    """
    Get the sentences that the word is in.
    """
    user_input = input("The system is ready, enter your text: \n").lower()
    match_sentences = {}
    words = user_input.split()

    if len(words) > 2:
        for x in range(len(words)):
            sentences_that_word_appears = words_trie.get_sentences_of_word(words[x])
            if sentences_that_word_appears:
                for k, v in sentences_that_word_appears.items():
                    if x == 0:
                        match_sentences[k] = 1
                    elif x == 1:
                        match_sentences[k] = match_sentences.get(k, 0) + 1
                    else:
                        if match_sentences.get(k, 0) is None:
                            match_sentences[k] = None
                        elif match_sentences.get(k, 0) >= x - 1:
                            match_sentences[k] += 1
                        else:
                            match_sentences[k] = None

        return [key for key, value in match_sentences.items() if value is not None and value >= len(words) - 1]
    else:
        return []


sentences_df = pd.DataFrame(columns=['sentence', 'file_path'])
words_trie = Trie()


def main():
    initialize_data()
    while True:
        print(run())


if __name__ == "__main__":
    main()
