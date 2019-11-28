import os
from flask import Flask, jsonify, request, Blueprint
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from sklearn.externals import joblib
from nltk.stem import WordNetLemmatizer
import nltk
#nltk.download('wordnet')

app = Flask(__name__)
api = Api(app)

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

# Helper functions & classifier models
lemmatizer = WordNetLemmatizer()

def vectorizer_lemmatized(text):
    return [lemmatizer.lemmatize(word, pos='v') for word in text.split() ]

def vectorizer(text):
    return text.split()

lr = joblib.load('models/lr.joblib')
mnb = joblib.load('models/mnb.joblib')
#svc = joblib.load('models/svc.joblib')
dt = joblib.load('models/dt.joblib')
# rf = joblib.load('rf.joblib')
# xgb = joblib.load('xgb.joblib')


# Endpoint for each model
class MakePredictionLR(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
        text = posted_data['text']

        prediction = lr.predict([text])[0]
        return jsonify({
            'Prediction': prediction
        })


class MakePredictionMNB(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
        text = posted_data['text']

        prediction = mnb.predict([text])[0]
        return jsonify({
            'Prediction': prediction
        })

# class MakePredictionSVC(Resource):
#     @staticmethod
#     def post():
#         posted_data = request.get_json()
#         text = posted_data['text']
#
#         prediction = svc.predict([text])[0]
#         return jsonify({
#             'Prediction': prediction
#         })

class MakePredictionDT(Resource):
    @staticmethod
    def post():
        posted_data = request.get_json()
        text = posted_data['text']

        prediction = dt.predict([text])[0]
        return jsonify({
            'Prediction': prediction
        })

# class MakePredictionRF(Resource):
#     @staticmethod
#     def post():
#         posted_data = request.get_json()
#         text = posted_data['text']
#
#         prediction = rf.predict([text])[0]
#         return jsonify({
#             'Prediction': prediction
#         })

# class MakePredictionXGB(Resource):
#     @staticmethod
#     def post():
#         posted_data = request.get_json()
#         text = posted_data['text']
#
#         prediction = xgb.predict([text])[0]
#         return jsonify({
#             'Prediction': prediction
#         })

# Adding endpoints to API
api.add_resource(MakePredictionLR, '/logistic-regression-predict')
api.add_resource(MakePredictionMNB, '/multinomial-naive-bayes-predict')
# api.add_resource(MakePredictionSVC, '/multinomial-naive-bayes-predict')
api.add_resource(MakePredictionDT, '/decision-tree-predict')
# api.add_resource(MakePredictionRF, '/random-forest-predict')
# api.add_resource(MakePredictionXGB, '/xgb-predict')


if __name__ == '__main__':
    app.run(debug=True)
