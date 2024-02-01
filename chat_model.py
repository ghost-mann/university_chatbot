#import necessary packages


# Importing the json module for working with JSON data
import json

# Importing the NumPy library with an alias 'np' for numerical operations
import numpy as np

# Importing the random module for generating random numbers
import random

# Importing the Natural Language Toolkit (nltk) for natural language processing tasks
import nltk

# Importing a custom module named 'utils' with an alias 'u'
import utils as u


# Commenting out the following lines as they are related to nltk data downloads,
# which can be uncommented if needed in the future.
# nltk.download('punkt')
# nltk.download('wordnet')

# Importing the Sequential model from the Keras library for building neural networks
from keras.models import Sequential

# Importing layers (Dense, Activation, Dropout) from Keras for building neural network layers
from keras.layers import Dense, Activation, Dropout

# Importing the Stochastic Gradient Descent (SGD) optimizer from Keras
from keras.optimizers import SGD

class ChatModel:
    def __init__(self):
        # Call tokenizing procedure
        # Tokenizing intents data from 'intents.json' and retrieving necessary variables
        w, words, documents, classes, self._intents = self.tokenizing('intents.json')

        # Call lemmatizing procedure
        # Lemmatizing words and documents using the lemmatizing procedure
        w, words, documents, classes, lemmatizer = self.lemmatizing(w, words, documents, classes)

        # Call training_data procedure
        # Preparing training data for the model using the training_data procedure
        self._train_x, self._train_y = self.training_data(w, words, documents, classes, lemmatizer)

        # Call tokenizing procedure
        # Training the model using the prepared training data
        self._model = self.training(self._train_x, self._train_y)

    # Getter method to retrieve the training input features
    def get_train_x(self):
        return self._train_x

    # Getter method to retrieve the training output labels
    def get_train_y(self):
        return self._train_y

    # Getter method to retrieve the trained model
    def get_model(self):
        return self._model

    # Getter method to retrieve the intents data
    def get_intents(self):
        return self._intents


import pickle

#Creation of pickle files to store all Python objects which we’ll use in the prediction process

def create_pickle(list, pkl_url):
    return pickle.dump(list, open(pkl_url, 'wb'))

def load_pickle(pkl_url):
    return pickle.load(open(pkl_url, 'rb'))

#load and preprocess data file
def tokenizing(self,url):
    words= []
    classes= []
    documents= []
    intents = json.loads(open(url).read())

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            #tokenize each word
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            #add documents in the corpus
            documents.append((w, intent['tag']))
            #add to our classes list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])
    return w, words, documents, classes, intents


def lemmatizing(self, w, words, documents, classes):
    ignore_words = ['?', '!']
    lemmatizer = nltk.stem.WordNetLemmatizer()
    # lemmatize, lower each word and remove duplicates
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
    # sort classes and words
    classes = sorted(list(set(classes)))
    words = sorted(list(set(words)))
    # documents = combination between patterns and intents
    print (len(documents), 'documents')
    # classes = intents
    print (len(classes), 'classes', classes)
    # words = all words, vocabulary
    print (len(words), 'unique lemmatized words', words)
    u.create_pickle(words, 'pickles\words.pkl')
    u.create_pickle(classes, 'pickles\classes.pkl')
    return w, words, documents, classes, lemmatizer

#create training and testing data
def training_data(self, w, words, documents, classes, lemmatizer):
    # create our training data
    training = []
    train_x = []
    train_y = []
    # create an empty array for our output
    output_empty = [0] * len(classes)

    # training set, bag of words for each sentence
    for doc in documents:

    # initialize our bag of words
        bag = []

    # list of tokenized words for the pattern
        pattern_words = doc[0]

    # lemmatize each word — create base word, in attempt to represent related words
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

    # create our bag of words array with 1, if word match found in current pattern
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

    # output is a ‘0’ for each tag and ‘1’ for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)

    # create train and test lists. X — patterns, Y — intents
    train_x = list(training[:,0])
    train_y = list(training[:,1])
    print("Training data created")
    return train_x, train_y

