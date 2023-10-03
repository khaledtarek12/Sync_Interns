import nltk
from nltk.chat.util import Chat  , reflections

reflections
# print(Chat)

set_pairs = [
    [
        r"my name is (.*)",
        ["hello %1 , How are you today?",]
    ],
    [
        r"hi|hey|hello",
        ["Hello" , 'Hey there',]
    ],
    [
        r"what is your name ?",
        ["You can call my a chatbot ?",]
    ],
    [
        r"How are you ?",
        ["I am fine , thank you ! How can i help you ?",]
    ],
    [
        r"I am fine , thank you",
        ["Great to hear that , How can i help you ?",]
    ],
    [
        r"How can i help you ?",
        ["i am looking for online guides and courses to learn data science , can you suggest some thing to me ?",]
    ],
    [
        r"i'm (.*) doing good",
        ["That's great to hear" , "how can i help you ? :)",]
    ],
    [
        r"i am looking for online guides and courses to learn data science , can you suggest some thing to me ?",
        ["elzero channel is a great option  to learn data science , you can check his channel"]
    ],
    [
        r"thank for the suggestion . do they have greate authors and instructors",
        ["yes , they have the world class best authors , that is their strength :)",]
    ],
    [
        r"(.*) thanks you so much , that was helpful",
        ["i'm happy to help" , "No problem , you are welcome",]
    ],
    [
        r"quit|end|thanks|goodbye|bye|see you soon",
        ["Bye , take care. see you soon :) ", "it was nice talking to you . see you soon :)"]
    ],
]

# def chatbot():
#     print("Hi I am a chatbot ! How can i help ?")
    
# chatbot()

# chat = Chat(set_pairs , reflections)
# print(chat)

# chat.converse()
# if __name__ == "__main__":
#     chatbot()



import nltk
import numpy as np
import random
import string
import bs4 as bs
import requests
import re
import warnings

warnings.filterwarnings = False
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# nltk.download('punkt')
# nltk.download('wordnet')
r = requests.get('https://en.wikipedia.org/wiki/Cuisine')
# print(r)
raw_html = r.text

corpus_html = bs.BeautifulSoup(raw_html)
courps_paras = corpus_html.find_all('p')
courps_txt = ''

for paras in courps_paras:
    courps_txt += paras.text

courps_txt = courps_txt.lower()
courps_txt = re.sub(r'\[[0-9]*\]', ' ' , courps_txt)
courps_txt = re.sub(r'\s+' , ' ' , courps_txt)
courps_sentences = nltk.sent_tokenize(courps_txt)
courps_wwords = nltk.word_tokenize(courps_txt)

greeting_inputs = ('hey' , 'good morning' , 'good evening' , 'morning' , 'evening' , 'hi' , 'whatsup')
greeting_responses = ['hey' , 'hey how are you' , 'Hello , how you doing' , 'Hello' , 'Welcome , iam good']

def choise_response(greeting):
    for token in greeting.split():
        if token.lower() in greeting_inputs:
            return random.choice(greeting_responses)

lemetizer = nltk.stem.WordNetLemmatizer()

def lemmtize_courps(tokens):
    return [lemetizer.lemmatize(token) for token in tokens]

remove_puncet  = dict((ord(punctuation) , None) for punctuation in string.punctuation)

def get_text(document):
    return lemmtize_courps(nltk.word_tokenize(document.lower().translate(remove_puncet)))


def responed(user_input):
    bot_response = ''
    courps_sentences.append(user_input)

    word_vectorize = TfidfVectorizer(tokenizer=get_text , stop_words='english')
    corpus_word_vector = word_vectorize.fit_transform(courps_sentences)
    
    cos_sim_vector = cosine_similarity(corpus_word_vector[-1] , corpus_word_vector)
    similitry_response_idx = cos_sim_vector.argsort()[0][-2]
    
    matched_vector = cos_sim_vector.flatten()
    matched_vector.sort()
    
    vector_matched = matched_vector[-2]
    
    if vector_matched == 0:
        bot_response  = bot_response + "I am sorry  , what is it , again?"
        return bot_response
    else:
        bot_response = bot_response + courps_sentences[similitry_response_idx]
        return bot_response

chat = True
print('Hello , what do you want to learn about Cuisines today ?')
while(chat == True):
    user_quary = input()
    user_quary = user_quary.lower()
    if user_quary != 'quit':
        if user_quary == 'thanks' or user_quary == ' thank you' :
            chat = False
            print('CuisineBot: You are Welcome! :)')
        else:
            if choise_response(user_quary) != None:
                print('CuisineBot: ' + choise_response(user_quary))
            else:
                print('CuisineBot: ' , end='')
                print(responed(user_quary))
                courps_sentences.remove(user_quary)
    else:
        chat = False
        print('CuisineBot: Good Bye! :)')