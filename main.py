import pandas as pd
import os
import time
from Trie import Trie
import logging
from calculate_score import calculate_scores, preprocess_sentence

# Define data directories and paths
DATA_DIR = "/Archive1"
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
ENGLISH_LETTERS_NUM = 26
logs_dir = os.path.join(CURR_DIR, "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, "application.log")

# Configure logging
logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log that the logging system has been initialized
logging.info("Logging system initialized.")

# Create a DataFrame to hold sentences and a Trie data structure for words
sentences_df = pd.DataFrame(columns=['sentence', 'file_path'])
words_trie = Trie()


def filter_sentences_input_smaller_than_2(input_string: str) -> object:
    input_string = preprocess_sentence(input_string)
    words = input_string.split()
    all_sentence_ids = []

    for word in words:
        word_sentence_ids = set()
        original_match_sentences = words_trie.get_sentences_of_word(word) or {}
        word_sentence_ids = word_sentence_ids.union(original_match_sentences.keys())

        for i in range(len(word)):

            for char_num in range(ENGLISH_LETTERS_NUM):
                add_char_before = word[:i] + chr(ord('a') + char_num) + word[i:]
                change_char = word[:i] + chr(ord('a') + char_num) + word[i + 1:]
                remove_char = word[:i] + word[i + 1:]

                match_sentences1 = words_trie.get_sentences_of_word(add_char_before) or {}
                match_sentences2 = words_trie.get_sentences_of_word(change_char) or {}
                match_sentences3 = words_trie.get_sentences_of_word(remove_char) or {}

                word_sentence_ids = word_sentence_ids.union(match_sentences1.keys(), match_sentences2.keys(),
                                                            match_sentences3.keys())

        for char_num in range(ENGLISH_LETTERS_NUM):
            add_char_end = word + chr(ord('a') + char_num)
            match_sentences_end = words_trie.get_sentences_of_word(add_char_end) or {}
            word_sentence_ids = word_sentence_ids.union(match_sentences_end.keys())

        if not all_sentence_ids:
            all_sentence_ids = word_sentence_ids
        else:
            all_sentence_ids = all_sentence_ids.intersection(word_sentence_ids)

    return [index - 1 for index in all_sentence_ids]


# Function to initialize the Trie with words from a sentence
def initialize_words_trie(line: str, sentence_id: int):
    words = line.split()
    for x in range(len(words)):
        words_trie.insert(words[x], sentence_id, x)


# Function to check if a line contains words
def contains_words(line):
    return any(c.isalpha() for c in line)


# Function to load data from files and populate data structures
def initialize_data():
    global sentences_df
    logging.info("Loading the files and preparing the system...")
    print("Loading files and preparing the system...")

    directory = CURR_DIR + DATA_DIR
    sentence_id = 1
    sentences = []

    # Walk through directory, read files, and process sentences
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(subdir, file)) as txt_file:
                    content = txt_file.read()
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if contains_words(line):
                            sentences.append([line, file])
                            initialize_words_trie(line, sentence_id)
                            sentence_id += 1

    sentences_df = pd.DataFrame(sentences)


# Main search function
def get_matches():
    """
    Get the sentences that the word is in.
    """
    user_input = input("The system is ready, enter your text: \n").lower()

    # Start timer for search time
    start_time = time.time()

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

        matching_sentence_ids = [key - 1 for key, value in match_sentences.items() if
                                 value is not None and value >= len(words) - 1]
        # Fetch the actual sentences from the DataFrame
        filtered_df = sentences_df[sentences_df.index.isin(matching_sentence_ids)]
        filtered_df.columns = ['sentence', 'file_path']
        # Stop timer for search
        end_time = time.time()
        runtime = end_time - start_time
        print(f"Program runtime: {runtime:.6f} seconds")

        return user_input, filtered_df
    else:
        matching_sentence_ids = filter_sentences_input_smaller_than_2(user_input)
        filtered_df = sentences_df[sentences_df.index.isin(matching_sentence_ids)]
        filtered_df.columns = ['sentence', 'file_path']
        return user_input, filtered_df


# Main Function
def main():
    # Load data files to datastructures
    initialize_data()
    print(sentences_df)

    while True:
        user_input, filtered_df = get_matches()
        top_results = calculate_scores(user_input, filtered_df)

        for idx, result in enumerate(top_results, start=1):
            print(f"Top Matches:\n Top {idx}: Source Text: {result.source_text}, Score: {result.score}")


# Entry point
if __name__ == "__main__":
    main()
