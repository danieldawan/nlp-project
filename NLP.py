def load_book(filename):
    """
    Loads the text from a file and returns a list of sentences, where each sentence is represented as a list of words.
    :param filename: The path to the text file to be read.
    :return: A list of sentences, with each sentence being a list of words.
    """
    corpus = []
    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                corpus.append(stripped_line.split(' '))
    return corpus

def get_corpus_length(corpus):
    """
    Calculates the total number of words in the corpus.
    :param corpus: The corpus as a list of sentences, with each sentence being a list of words.
    :return: The total count of words in the corpus.
    """
    count = 0
    for sentence in corpus:
        count += len(sentence)
    return count

def build_vocabulary(corpus):
    """
    Builds a vocabulary set from the corpus, containing all unique words.
    :param corpus: The corpus as a list of sentences, with each sentence being a list of words.
    :return: A list of unique words in the corpus.
    """
    vocabulary = set()
    for sentence in corpus:
        for word in sentence:
            vocabulary.add(word)
    return list(vocabulary)

def count_unigrams(corpus):
    """
    Counts the occurrence of each word in the corpus.
    :param corpus: The corpus as a list of sentences, with each sentence being a list of words.
    :return: A dictionary with words as keys and their counts as values.
    """
    unigram_counts = {}
    for sentence in corpus:
        for word in sentence:
            if word in unigram_counts:
                unigram_counts[word] += 1
            else:
                unigram_counts[word] = 1
    return unigram_counts

def make_start_corpus(corpus):
    """
    Identifies and collects the starting words of all sentences in the corpus.
    :param corpus: The corpus as a list of sentences, with each sentence being a list of words.
    :return: A list of unique starting words in the corpus.
    """
    start_words = set()
    for sentence in corpus:
        if sentence:
            start_words.add(sentence[0])
    return list(start_words)

def count_bigrams(corpus):
    """
    Counts occurrences of bigrams (pairs of consecutive words) in the corpus.
    :param corpus: The corpus as a list of sentences, with each sentence being a list of words.
    :return: A dictionary where keys are the first words of bigrams, and values are dictionaries of the second words and their counts.
    """
    bigram_counts = {}
    for sentence in corpus:
        for i in range(len(sentence)-1):
            if sentence[i] in bigram_counts:
                if sentence[i+1] in bigram_counts[sentence[i]]:
                    bigram_counts[sentence[i]][sentence[i+1]] += 1
                else:
                    bigram_counts[sentence[i]][sentence[i+1]] = 1
            else:
                bigram_counts[sentence[i]] = {sentence[i+1]: 1}
    return bigram_counts

def build_uniform_probs(start_words):
    """
    Creates a uniform probability distribution for the starting words.
    :param start_words: A list of starting words.
    :return: A list of probabilities, equal for each starting word.
    """
    uniform_prob = 1 / len(start_words)
    return [uniform_prob] * len(start_words)

def build_unigram_probs(unigrams, unigram_counts, total_count):
    """
    Calculates the probability of each unigram in the corpus based on its frequency.
    :param unigrams: A list of unique words in the corpus.
    :param unigram_counts: A dictionary with words as keys and their counts as values.
    :param total_count: The total count of words in the corpus.
    :return: A list of probabilities corresponding to the unigrams.
    """
    unigram_probs = []
    for unigram in unigrams:
        unigram_count = unigram_counts.get(unigram, 0)
        unigram_prob = unigram_count / total_count
        unigram_probs.append(unigram_prob)
    return unigram_probs

def build_bigram_probs(unigram_counts, bigram_counts):
    """
    Calculates the conditional probability of each bigram in the corpus.
    :param unigram_counts: A dictionary with words as keys and their counts as values.
    :param bigram_counts: A dictionary where keys are the first words of bigrams, and values are dictionaries of the second words and their counts.
    :return: A dictionary where keys are the first words of bigrams and values are dictionaries containing the following words and their probabilities.
    """
    bigram_probs = {}
    for prev_word in bigram_counts:
        following_words = []
        probs = []
        for word in bigram_counts[prev_word]:
            following_words.append(word)
            prob = bigram_counts[prev_word][word] / unigram_counts[prev_word]
            probs.append(prob)
        temp_dict = {"words": following_words, "probs": probs}
        bigram_probs[prev_word] = temp_dict
    return bigram_probs

def get_top_words(count, words, probs, ignore_list):
    """
    Retrieves the top words based on their probability, excluding any in the ignore list.
    :param count: The number of top words to return.
    :param words: A list of words to consider.
    :param probs: A list of probabilities corresponding to each word.
    :param ignore_list: A list of words to exclude from consideration.
    :return: A dictionary of the top words and their probabilities.
    """
    word_probs = {word: prob for word, prob in zip(words, probs) if word not in ignore_list}
    sorted_word_probs = dict(sorted(word_probs.items(), key=lambda item: item[1], reverse=True))
    top_words = dict(list(sorted_word_probs.items())[:count])
    return top_words

from random import choices
def generate_text_from_unigrams(count, words, probs):
    """
    Generates text by randomly selecting words based on their unigram probabilities.
    :param count: The number of words to generate.
    :param words: A list of words to choose from.
    :param probs: A list of probabilities corresponding to each word.
    :return: A string of generated text.
    """
    text = ''
    for _ in range(count):
        word = choices(words, weights=probs)[0]
        text += ' ' + word
    return text.lstrip()

def generate_text_from_bigrams(count, start_words, start_word_probs, bigram_probs):
    """
    Generates text by selecting words based on bigram probabilities, starting with a randomly chosen start word.
    :param count: The number of words to generate.
    :param start_words: A list of potential starting words.
    :param start_word_probs: The probabilities for each start word.
    :param bigram_probs: The bigram probabilities.
    :return: A string of generated text.
    """
    text = ''
    last_word = '.'
    for _ in range(count):
        if last_word == '.':
            word = choices(start_words, weights=start_word_probs)[0]
        else:
            next_words = bigram_probs.get(last_word, {'words': start_words, 'probs': start_word_probs})['words']
            next_probs = bigram_probs.get(last_word, {'words': start_words, 'probs': start_word_probs})['probs']
            word = choices(next_words, weights=next_probs)[0]
        text += ' ' + word
        last_word = word
    return text.lstrip()

def main():
    # Main function to orchestrate the text generation process.
    pass

if __name__ == "__main__":
    main()