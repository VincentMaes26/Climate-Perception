import os
from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
import sklearn
import sys
import joblib
import pickle
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

def vectorizer_lemmatized(text):
    return [lemmatizer.lemmatize(word, pos='v') for word in text.split() ]

def vectorizer(text):
    return text.split()

app = Flask(__name__)

# Swagger configuration
SWAGGER_URL = '/api-docs'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "classifier-model-api"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

# Helper functions


def get_prediction(model):
    posted_data = request.get_json()
    text = posted_data['text']
    prediction = model.predict([text])[0]
    return jsonify({
        'Prediction': prediction
    })



# routes
@app.route('/logistic-regression-predict', methods=['POST'])
def PredictLR():
    with open('models/lr.joblib', 'rb') as f:
        lr = joblib.load(f)

    prediction = get_prediction(lr)
    return prediction

@app.route('/multinomial-naive-bayes-predict', methods=['POST'])
def PredictMNB():
    with open('models/mnb.joblib', 'rb') as f:
        mnb = joblib.load(f)

    prediction = get_prediction(mnb)
    return prediction

@app.route('/decision-tree-predict', methods=['POST'])
def PredictDT():
    with open('models/dt.joblib', 'rb') as f:
        dt = joblib.load(f)
    prediction = get_prediction(dt)
    return prediction

if __name__ == '__main__':
    app.run(debug=True)
    
