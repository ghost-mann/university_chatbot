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

# build the model
def training(self,train_x, train_y):
# sequential from keras
# create model- 3 layers, First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to the number of intents to predict output intent with softmax
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

# compile model, stochastic gradient descent with nesterov accelerated gradient gives good results for this model
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd,metrics=['accuracy'])
# fitting and saving the model
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
    model.save('chatbot_model.h5', hist)
    print("modeseql created")
    return model

#predicted responses
from chat_model import ChatModel as chatModel
import nltk
import pickle
import numpy as np
from keras.models import load_model
import json
import random
import utils as u

class ChatApp:

    def __init__(self):
        self.cM = chatModel()
        self._lemmatizer = nltk.stem.WordNetLemmatizer()
        self._model = load_model('chatbot_model.h5')
        self._intents = self.cM.get_intents()
        self._words = u.load_pickle('pikles\words.pkl')
        self._classes = u.load_pickle('pickles\classes.pkl')

    #provide input data
    def clean_up_sentence(self,sentence):
        # tokenize the pattern - split words into array
        sentence_words = nltk.word_tokenize(sentence)
    # stem each wor - create short form for word
        sentence_words = [self._lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words
    #return existing bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    def bow(self, sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    # assign 1 if the current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
                        return(np.array(bag))
                    def predict_class(self, sentence, model):
                        ERROR_THRESHOLD = 0.25
                    # filter out predictions below a threshold
                        p = self.bow(sentence, self._words, show_details=False)
                        res = self._model.predict(np.array([p]))[0]
                        results = [[i,r] for i,r in enumerate(res) if r >ERROR_THRESHOLD]
                    # sort by strength of probability
                        results.sort(key=lambda x: x[1], reverse=True)
                        return_list = []
                        for r in results:
                            return_list.append({"intent": self._classes[r[0]], "probability": str(r[1])})
                            return return_list

    #random response from list of intents
    def getResponse(self, ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
                return result
    def chatbot_response(self, text):
        ints = self.predict_class(text, self._model)
        res = self.getResponse(ints, self._intents)
        return res




#Creating GUI with tkinter
import tkinter
from tkinter import *
from .chatapp import ChatApp as cA

def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    if msg != '':
            ChatLog.config(state=NORMAL)
            ChatLog.insert(END, "You: " + msg + '\n\n')
            ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
            res = cA().chatbot_response(msg)
            ChatLog.insert(END, "Bot: " + res + '\n\n')
            ChatLog.config(state=DISABLED)
            ChatLog.yview(END)


base = Tk()
base.title("ChatBot - SL")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)
#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )
#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)

#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

base.mainloop()