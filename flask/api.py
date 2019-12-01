import os
from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
#from sklearn.externals
import joblib
from nltk.stem import WordNetLemmatizer
import nltk
#nltk.download('wordnet')

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

# Helper functions
lemmatizer = WordNetLemmatizer()

def vectorizer_lemmatized(text):
    return [lemmatizer.lemmatize(word, pos='v') for word in text.split() ]

def vectorizer(text):
    return text.split()

def get_prediction(model):
    posted_data = request.get_json()
    text = posted_data['text']
    prediction = model.predict([text])[0]
    return jsonify({
        'Prediction': prediction
    })


# Loading in the trained classifiers
lr = joblib.load('models/lr.joblib')
mnb = joblib.load('models/mnb.joblib')
#svc = joblib.load('models/svc.joblib')
dt = joblib.load('models/dt.joblib')
# rf = joblib.load('rf.joblib')
# xgb = joblib.load('xgb.joblib')

# routes
@app.route('/logistic-regression-predict', methods=['POST'])
def PredictLR():
    prediction = get_prediction(lr)
    return prediction

@app.route('/multinomial-naive-bayes-predict', methods=['POST'])
def PredictLR():
    prediction = get_prediction(mnb)
    return prediction

@app.route('/decision-tree-predict', methods=['POST'])
def PredictLR():
    prediction = get_prediction(dt)
    return prediction

if __name__ == '__main__':
    app.run(debug=True)
