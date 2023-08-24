import pandas as pd
import os
from Trie import Trie
import logging
from calculate_score import calculate_scores, AutoCompleteData

DATA_DIR = "/Archive2"
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
logs_dir = os.path.join(CURR_DIR, "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

log_file_path = os.path.join(logs_dir, "application.log")

logging.basicConfig(filename=log_file_path,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Test the logging setup
logging.info("Logging system initialized.")


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
    logging.info("Loading the file and preparing the system...")
    print("Loading the file and preparing the system...")
    directory = CURR_DIR + DATA_DIR
    counter = 1
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                print(f'reading file number {counter}')
                with open(os.path.join(subdir, file), encoding='utf-8') as txt_file:
                    content = txt_file.read()
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if contains_words(line):
                            sentence_id = initialize_sentences_dataframe(line, file)
                            initialize_words_trie(line, sentence_id)
                counter += 1


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

        matching_sentence_ids = [key - 1 for key, value in match_sentences.items() if
                                 value is not None and value >= len(words) - 1]
        # Fetch the actual sentences from the dataframe
        filtered_df = sentences_df[sentences_df.index.isin(matching_sentence_ids)]

        return user_input, filtered_df
    else:
        return user_input, pd.DataFrame(columns=['sentence', 'file_path'])


sentences_df = pd.DataFrame(columns=['sentence', 'file_path'])
words_trie = Trie()


def main():
    initialize_data()
    while True:
        try:
            user_input, filtered_df = run()
            top_results = calculate_scores(user_input, filtered_df)

            for idx, result in enumerate(top_results, start=1):
                print(f"Top {idx}: Source Text: {result.source_text}, Score: {result.score}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
