import json
from flask import Flask, request, redirect
from flask_expects_json import expects_json
from functions import SurveyAPI

app = Flask(__name__)
app.config["DEBUG"] = True

schema = {
    'response': 'string',
    'survey_id': 'string'
    }

@app.route('/survey', methods=['GET'])
def getRedirect():
    if request.method == "GET":
        data = request.get_json()
        current_survey = data['survey']['survey_id']
        return redirect(f"survey/{current_survey}", code=303)

@expects_json(schema)
@app.route('/response', methods=['POST'])
def surveyReceived():
    SurveyAPI.receiveSurvey(request)
    return "Survey Sent!"

@app.route(f"/survey/COVID-19")
def htmlSurveys():
    return SurveyAPI.getCovidSurvey()


app.run()