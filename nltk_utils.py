import nltk 
from nltk.stem.porter import PorterStemmer
import numpy as np

stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words):
    """
    This function will return an array with 0 and 1 based on the correspondance of tokenized words passed as an argument
    and the existance of each word in the all_words array. The result array is based on the all_words array positions.
    """
    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32)

    for idx, word in enumerate(all_words):
        if word in tokenized_sentence:
            bag[idx] = 1.0
    
    return bag