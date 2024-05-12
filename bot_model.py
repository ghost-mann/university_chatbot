# Import all packages we'll need.
import json
import numpy as np
import random
import nltk
import utils as u
nltk.download('punkt')
nltk.download('wordnet')
import mysql.connector

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD


class ChatModel:

    def __init__(self):
        # Call tokenizing procedure
        w, words, documents, classes, self._intents = self.tokenizing()

        # Call lemmatizing procedure
        w, words, documents, classes, lemmatizer = self.lemmatizing(w, words, documents, classes)

        # Call training_data procedure
        self._train_x, self._train_y = self.training_data(w, words, documents, classes, lemmatizer)

        # Call tokenizing procedure
        self._model = self.training(self._train_x, self._train_y)

    def tokenizing(self):
        words = []
        classes = []
        documents = []
        intents = []

        # Connect to the database
        db = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="root",
            database="chatbot"
        )

        # Create a cursor object
        cursor = db.cursor()

        # Fetch intents data from the database
        query = "SELECT tag, patterns, responses FROM intents"
        cursor.execute(query)
        result = cursor.fetchall()

        for row in result:
            intent_tag = row[0]
            intent_pattern = row[1]
            intent_responses = row[2].split('|')  # Assuming responses are separated by '|'

            # tokenize the pattern
            w = nltk.word_tokenize(intent_pattern)
            words.extend(w)
            # add documents in the corpus
            documents.append((w, intent_tag))
            # add to our classes list
            if intent_tag not in classes:
                classes.append(intent_tag)

            intents.append({"tag": intent_tag, "patterns": [intent_pattern], "responses": intent_responses})

        # Close the database connection
        db.close()

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
        print(len(documents), "documents")

        # classes = intents
        print(len(classes), "classes", classes)

        # words = all words, vocabulary
        print(len(words), "unique lemmatized words", words)

        u.create_pickle(words, 'pickles\words.pkl')
        u.create_pickle(classes, 'pickles\classes.pkl')
        return w, words, documents, classes, lemmatizer

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
            # lemmatize each word - create base word, in an attempt to represent related words
            pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
            # create our bag of words array with 1, if word match found in the current pattern

            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)

            # output is a '0' for each tag and '1' for the current tag (for each pattern)
            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1
            training.append((bag, output_row))

        # shuffle our features and turn into np.array
        random.shuffle(training)

        # Separate the features (bag) and labels (output_row) into two lists
        train_x = [item[0] for item in training]
        train_y = [item[1] for item in training]

        print("Training data created")
        return train_x, train_y

    def training(self, train_x, train_y):
        # Sequential from Keras Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd
        # output layer contains the number of neurons equal to the number of intents to predict output intent with
        # softmax
        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this
        # model
        sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)  # Adjusted for the new Keras syntax
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        # fitting and saving the model
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        model.save('chatbot_model.h5', hist)
        print("modeseql created")

        return model

    def get_train_x(self):
        return self._train_x

    def get_train_y(self):
        return self._train_y

    def get_model(self):
        return self._model

    def get_intents(self):
        return self._intents
