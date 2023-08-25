from dataclasses import dataclass
import string
import Levenshtein


ERR_ADDITION = "addition"
ERR_SUBTRACTION = "deletion"
ERR_REPLACEMENT = "substitution"


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    file_path: str
    offset: int
    score: int


def preprocess_sentence(sentence):
    # Remove punctuation and convert to lowercase
    translator = str.maketrans("", "", string.punctuation)
    sentence = sentence.translate(translator).lower()
    return sentence


def increment_score(score, word):
    return score + len(word) * 2


def calculate_penalty(position, penalty_type):
    if penalty_type == ERR_REPLACEMENT:
        if position == 0:
            return 5
        elif position == 1:
            return 4
        elif position == 2:
            return 3
        elif position == 3:
            return 2
        else:
            return 1
    elif penalty_type == ERR_ADDITION or penalty_type == ERR_SUBTRACTION:
        if position == 0:
            return 10
        elif position == 1:
            return 8
        elif position == 2:
            return 6
        elif position == 3:
            return 4
        else:
            return 2
    else:
        return 0


def penalty_score(sentence, sentence_word, user_word, score, penalty_type):
    if sentence_word not in sentence:
        return score

    position = sentence.index(sentence_word)

    if user_word == sentence_word:
        return score

    penalty = calculate_penalty(position, penalty_type)
    return score - penalty


def calculate_change_type(user_word, sentence_word):
    levenshtein_distance = Levenshtein.distance(user_word, sentence_word)
    if levenshtein_distance == 1:
        if len(user_word) == len(sentence_word):
            return ERR_REPLACEMENT
        elif len(user_word) < len(sentence_word):
            return ERR_SUBTRACTION
        else:
            return ERR_ADDITION
    return None


def update_results_list(results_list, new_data, min_top_score):
    if len(results_list) < 5:
        results_list.append(new_data)
        if new_data.score < min_top_score:
            min_top_score = new_data.score
    elif new_data.score > min_top_score:
        min_score_index = min(enumerate(results_list), key=lambda x: x[1].score)[0]
        results_list[min_score_index] = new_data
        min_top_score = min(results_list, key=lambda x: x.score).score
    return results_list, min_top_score


def calculate_scores(user_sentence, sentences_df):
    autocomplete_results = []

    user_sentence = preprocess_sentence(user_sentence)
    user_words = user_sentence.split()

    for index, row in sentences_df.iterrows():
        position = 0
        score = 0
        one_change_found = False
        offset = 0
        processed_sentence = preprocess_sentence(row['sentence'])
        processed_sentence = processed_sentence.split()
        for word in user_words:
            if word in processed_sentence[position:]:
                score = increment_score(score, word)
                position = processed_sentence.index(word)
                if user_words.index(word) == 0:
                    offset = position+1
            elif not one_change_found:
                for i, sentence_word in enumerate(processed_sentence[position:]):
                    change_type = calculate_change_type(word, sentence_word)
                    if change_type:
                        score = penalty_score(processed_sentence, sentence_word, word, score, change_type)
                        one_change_found = True
                        position = processed_sentence.index(sentence_word)
                        break
                    else:
                        score = float('-inf')
            else:
                score = float('-inf')
                continue
        score = score + (2 * len(processed_sentence) - 1)  # add the score of the spaces in the sentence
        autocomplete_results.append(AutoCompleteData(user_sentence, row['sentence'], row['file_path'], offset, score))

    autocomplete_results.sort(key=lambda x: x.score, reverse=True)
    top_results = autocomplete_results[:5]

    return top_results
