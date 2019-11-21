import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from sklearn.externals import joblib
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')

app = Flask(__name__)
api = Api(app)

lemmatizer = WordNetLemmatizer()

def vectorizer_lemmatized(text):
    return [lemmatizer.lemmatize(word, pos='v') for word in text.split() ]

def vectorizer(text):
    return text.split()

lr = joblib.load('lr.joblib')
# mnb = joblib.load('mnb.joblib')
# svc = joblib.load('svc.joblib')
# dt = joblib.load('dt.joblib')
# rf = joblib.load('rf.joblib')
# xgb = joblib.load('xgb.joblib')


class MakePrediction(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
        text = posted_data['text']

        prediction = lr.predict([text])[0]
        return jsonify({
            'Prediction': prediction
        })


api.add_resource(MakePrediction, '/predict')


if __name__ == '__main__':
    app.run(debug=True)
