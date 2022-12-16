# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired

import urllib.request
import json


# initialize our Flask application and the model
app = flask.Flask(__name__)

app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    # load the pre-trained model
    global model
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    print(model)


# modelpath = "app/models/catboost_pipeline.dill"
modelpath = "models/catboost_pipeline.dill"
load_model(modelpath)


@app.route("/")
def index():
    return render_template('index.html')
#
# @app.route("/", methods=["GET"])
# def general():
#     return """Welcome magic predictor. Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the view
    data = {'success': False}
    curr_time = strftime('[%Y-%b-%d %H:%M:%S]')

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == 'POST':
        request_json = flask.request.get_json()

        print(request_json)
        input_data = pd.DataFrame({
            'Wife_age': int(request_json.get('Wife_age', '')),
            'Wife_education': int(request_json.get('Wife_education', '')),
            'Husband_education': int(request_json.get('Husband_education', '')),
            'Children': int(request_json.get('Children', '')),
            'Religion': int(request_json.get('Religion', '')),
            'Working': int(request_json.get('Working', '')),
            'Husband_Work': int(request_json.get('Husband_Work', '')),
            'Standard_of_living': int(request_json.get('Standard_of_living', '')),
            'Media_exposure': int(request_json.get('Media_exposure', '')),
        }, index=[0])

        try:
            # Predict the result
            preds = model.predict_proba(input_data)

        except AttributeError as e:
            logger.warning(f'{curr_time} Exception: {str(e)}')
            data['predictions'] = str(e)
            # Request unsuccessful
            data['success'] = False

        data['predictions'] = round(preds[:, 1][0], 5)
        # Request successful
        data['success'] = True

    return flask.jsonify(data)


class ClientDataForm(FlaskForm):
    Wife_age = StringField('Wife_age', validators=[DataRequired()])
    Wife_education = StringField('Wife_education', validators=[DataRequired()])
    Husband_education = StringField('Husband_education', validators=[DataRequired()])
    Children = StringField('Children', validators=[DataRequired()])
    Religion = StringField('Religion', validators=[DataRequired()])
    Working = StringField('Working', validators=[DataRequired()])
    Husband_Work = StringField('Husband_Work', validators=[DataRequired()])
    Standard_of_living = StringField('Standard_of_living', validators=[DataRequired()])
    Media_exposure = StringField('Media_exposure', validators=[DataRequired()])


def get_prediction(Wife_age, Wife_education, Husband_education,
                   Children, Religion, Working, Husband_Work, Standard_of_living, Media_exposure):
    print(Standard_of_living)
    body = {'Wife_age': Wife_age,
             'Wife_education': Wife_education,
             'Husband_education': Husband_education,
             'Children': Children,
             'Religion': Religion,
             'Working': Working,
             'Husband_Work': Husband_Work,
             'Standard_of_living': Standard_of_living,
             'Media_exposure': Media_exposure}

    myurl = "http://172.20.10.7:8181/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    # print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['Wife_age'] = request.form.get('Wife_age')
        data['Wife_education'] = request.form.get('Wife_education')
        data['Husband_education'] = request.form.get('Husband_education')
        data['Children'] = request.form.get('Children')
        data['Religion'] = request.form.get('Religion')
        data['Working'] = request.form.get('Working')
        data['Husband_Work'] = request.form.get('Husband_Work')
        data['Standard_of_living'] = request.form.get('Standard_of_living')
        data['Media_exposure'] = request.form.get('Media_exposure')

        try:
            response = str(get_prediction(data['Wife_age'],
                                            data['Wife_education'],
                                            data['Husband_education'],
                                            data['Children'],
                                            data['Religion'],
                                            data['Working'],
                                            data['Husband_Work'],
                                            data['Standard_of_living'],
                                            data['Media_exposure']))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181, debug=True)




