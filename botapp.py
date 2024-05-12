# Import necessary libraries and modules
from bot_model import ChatModel as chatModel
import nltk
import pickle
import numpy as np
from keras.models import load_model
import json
import random
import utils as u

# Define the ChatApp class
class ChatApp:

    # Initialize the ChatApp instance
    def __init__(self):
        # Create an instance of the ChatModel class
        self.cM = chatModel()
        # Initialize the WordNet Lemmatizer from NLTK
        self._lemmatizer = nltk.stem.WordNetLemmatizer()
        # Load the pre-trained chatbot model
        self._model = load_model('chatbot_model.h5')
        # Get the intents from the ChatModel instance
        self._intents = self.cM.get_intents()
        # Load pre-processed words and classes from pickles
        self._words = u.load_pickle('pickles\words.pkl')
        self._classes = u.load_pickle('pickles\classes.pkl')

    # Clean up a sentence by tokenizing and lemmatizing words
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self._lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # Convert a sentence to a bag of words (binary representation)
    def bow(self, sentence, words, show_details=True):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return np.array(bag)

    # Predict the intent class for a given sentence using the trained model
    def predict_class(self, sentence, model):
        ERROR_THRESHOLD = 0.25
        p = self.bow(sentence, self._words, show_details=False)
        res = self._model.predict(np.array([p]))[0]

        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = [{"intent": self._classes[r[0]], "probability": str(r[1])} for r in results]
        return return_list

    # Get a response based on the predicted intent
    def getResponse(self, ints, intents):
        tag = ints[0]['intent']
        for intent in intents:
            if intent['tag'] == tag:
                result = random.choice(intent['responses'])
                break
        return result
    # Get a response from the chatbot for a given input text
    def chatbot_response(self, text):
        ints = self.predict_class(text, self._model)
        res = self.getResponse(ints, self._intents)
        return res
