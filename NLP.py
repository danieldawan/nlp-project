def load_book(filename):
    corpus = []
    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                corpus.append(stripped_line.split(' '))
    return corpus

def get_corpus_length(corpus):
    count = 0
    for sentence in corpus:
        count += len(sentence)
    return count

def build_vocabulary(corpus):
    vocabulary = set()
    for sentence in corpus:
        for word in sentence:
            vocabulary.add(word)
    return list(vocabulary)

def count_unigrams(corpus):
    unigram_counts = {}
    for sentence in corpus:
        for word in sentence:
            if word in unigram_counts:
                unigram_counts[word] += 1
            else:
                unigram_counts[word] = 1
    return unigram_counts

def make_start_corpus(corpus):
    start_words = set()
    for sentence in corpus:
        if sentence:
            start_words.add(sentence[0])
    return list(start_words)

def count_bigrams(corpus):
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

def count_trigrams(corpus):
    trigram_counts = {}
    for sentence in corpus:
        for i in range(len(sentence) - 2):
            key = (sentence[i], sentence[i+1])
            if key in trigram_counts:
                if sentence[i+2] in trigram_counts[key]:
                    trigram_counts[key][sentence[i+2]] += 1
                else:
                    trigram_counts[key][sentence[i+2]] = 1
            else:
                trigram_counts[key] = {sentence[i+2]: 1}
    return trigram_counts

def build_uniform_probs(start_words):
    uniform_prob = 1 / len(start_words)
    return [uniform_prob] * len(start_words)

def build_unigram_probs(unigrams, unigram_counts, total_count):
    unigram_probs = []
    for unigram in unigrams:
        unigram_count = unigram_counts.get(unigram, 0)
        unigram_prob = unigram_count / total_count
        unigram_probs.append(unigram_prob)
    return unigram_probs

def build_bigram_probs(unigram_counts, bigram_counts):
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

from random import choices

def generate_text_from_unigrams(count, words, probs):
    text = ''
    for _ in range(count):
        word = choices(words, weights=probs)[0]
        text += ' ' + word
    return text.lstrip()

def generate_text_from_bigrams(count, start_words, start_word_probs, bigram_probs):
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

def generate_text_from_trigrams(count, start_words, bigram_probs, trigram_counts):
    """
    Generates text by selecting words based on trigram probabilities.
    :param count: The number of words to generate.
    :param start_words: A list of potential starting words.
    :param bigram_probs: The bigram probabilities.
    :param trigram_counts: The trigram counts.
    :return: A string of generated text.
    """
    if count < 3:
        return " ".join(choices(start_words, k=count))
    text = choices(start_words, k=2)  # Starting with two random words
    for _ in range(count - 2):
        last_two_words = tuple(text[-2:])
        if last_two_words in trigram_counts:
            next_words = list(trigram_counts[last_two_words].keys())
            next_probs = [trigram_counts[last_two_words][word] for word in next_words]
            next_word = choices(next_words, weights=next_probs, k=1)[0]
        else:
            # Fallback to bigram or even unigram probabilities if no trigram is found
            next_words = bigram_probs.get(last_two_words[1], {'words': start_words})['words']
            next_probs = bigram_probs.get(last_two_words[1], {'probs': [1/len(start_words)] * len(start_words)})['probs']
            next_word = choices(next_words, weights=next_probs, k=1)[0]
        text.append(next_word)
    return ' '.join(text)

def main():
    filename = './commedia.txt'
    num_words = 1000

    corpus = load_book(filename)
    corpus_length = get_corpus_length(corpus)
    vocabulary = build_vocabulary(corpus)
    unigram_counts = count_unigrams(corpus)
    start_corpus = make_start_corpus(corpus)
    bigram_counts = count_bigrams(corpus)
    trigram_counts = count_trigrams(corpus)
    unigram_probs = build_unigram_probs(vocabulary, unigram_counts, corpus_length)
    bigram_probs = build_bigram_probs(unigram_counts, bigram_counts)
    start_word_probs = build_uniform_probs(start_corpus)

    print("Generating text from unigrams...")
    text_from_unigrams = generate_text_from_unigrams(num_words, vocabulary, unigram_probs)
    print(text_from_unigrams)

    print("\nGenerating text from bigrams...")
    text_from_bigrams = generate_text_from_bigrams(num_words, start_corpus, start_word_probs, bigram_probs)
    print(text_from_bigrams)

    print("\nGenerating text from trigrams...")
    text_from_trigrams = generate_text_from_trigrams(num_words, start_corpus, bigram_probs, trigram_counts)
    print(text_from_trigrams)

if __name__ == "__main__":
    main()