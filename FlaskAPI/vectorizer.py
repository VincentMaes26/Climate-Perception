from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def vectorizer_lemmatized(text):
    return [lemmatizer.lemmatize(word, pos='v') for word in text.split() ]

def vectorizer(text):
    return text.split()
