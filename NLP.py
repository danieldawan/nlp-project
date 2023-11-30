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
  start_words = []
  for sentence in corpus:
    start_words.append([sentence[0]])
  return start_words

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

def build_uniform_probs(unigrams):
  unigram_probs = []
  for i in range(len(unigrams)):
    unigram_probs.append(1/len(unigrams))
  return unigram_probs

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

def get_top_words(count, words, probs, ignore_list):
  word_probs = {word: prob for word, prob in zip(words, probs) if word not in ignore_list}
  sorted_word_probs = dict(sorted(word_probs.items(), key=lambda item: item[1], reverse=True))
  top_words = dict(list(sorted_word_probs.items())[:count])
  return top_words

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
      next_words = bigram_probs[last_word]['words']
      next_probs = bigram_probs[last_word]['probs']
      word = choices(next_words, weights=next_probs)[0]
    text += ' ' + word
    last_word = word
  return text.lstrip()