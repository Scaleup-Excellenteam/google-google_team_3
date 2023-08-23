from dataclasses import dataclass
import pandas as pd
import numpy as np
import Levenshtein
import string


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


def calculate_score(base_score, position):
    if position == 0:
        return base_score * 2
    elif position == 1:
        return base_score * 2 - 1
    elif position == 2:
        return base_score * 2 - 2
    elif position == 3:
        return base_score * 2 - 3
    else:
        return base_score * 2 - 4


def preprocess_sentence(sentence):
    # Remove punctuation and convert to lowercase
    translator = str.maketrans("", "", string.punctuation)
    sentence = sentence.translate(translator).lower()
    return sentence


def calculate_auto_complete_data(user_sentence, sentences_df):
    autocomplete_results = []

    user_sentence = preprocess_sentence(user_sentence)
    words = user_sentence.split()

    for index, row in sentences_df.iterrows():
        processed_sentence = preprocess_sentence(row['sentence'])
        for word in words:
            if word in processed_sentence:
                base_score = len(word) * 2

                offset = processed_sentence.index(word)
                score = calculate_score(base_score, offset)

                autocomplete_results.append(
                    AutoCompleteData(word, row['sentence'], offset, score)
                )

    for index, row in sentences_df.iterrows():
        processed_sentence = preprocess_sentence(row['sentence'])
        for word in words:
            distance = Levenshtein.distance(word, processed_sentence)
            if distance == 1:
                offset = processed_sentence.index(word)
                if offset == 0:
                    score = calculate_score(10, offset)
                elif offset == 1:
                    score = calculate_score(8, offset)
                elif offset == 2:
                    score = calculate_score(6, offset)
                elif offset == 3:
                    score = calculate_score(4, offset)
                else:
                    score = calculate_score(2, offset)

                autocomplete_results.append(
                    AutoCompleteData(word, row['sentence'], offset, score)
                )

    autocomplete_results.sort(key=lambda x: x.score, reverse=True)
    top_results = autocomplete_results[:5]

    return top_results
