from tinydb import TinyDB, Query
from collections import Counter 
import json

### Initiate DB
db = TinyDB('db.json')

'''
TOOLS
'''
def findFrequentZips():
    '''
    Sort list of surveys by most recent zips
    '''
    results = db.all()
    zip_counter = Counter(d['zipcode'] for d in results)
    results = db.all()
    zipcode_list = zip_counter.most_common(len(results) + 1)
    return zipcode_list

class SurveyAPI:
    
    def receiveSurvey(request):
        '''
        Handle surveys and parse them'
        Store survey
        '''
        print(f"HERE HERE {request}")
        if request.is_json:
            request = request.get_json()
            survey = {"response": request['response']['response'], "survey_id": request['response']['survey_id'], "zipcode": request['response']['zipcode']}
            db.insert(survey)
        else:
            return "No JSON"


    def getCovidSurvey():
        '''
        Parse surveyId
        GET from storage
        Sort most frequent zipcodes
        Return HTML lists
        '''
        zipcode_list_html = []
        most_frequent_zipcode = findFrequentZips()
        for survey in range(0, len(most_frequent_zipcode)):
            zipcode_text = f"<li>Zipcode {most_frequent_zipcode[survey][0]} was used {most_frequent_zipcode[survey][1]} times</li>"
            zipcode_list_html.append(zipcode_text)
        print(zipcode_list_html)
        results = db.all()
        list_of_surveys = []
        for survey in results:
            response = survey['response']
            survey_id = survey['survey_id']
            zipcode = survey['zipcode']
            survey = f"<li>Response {response} with Survey Id {survey_id} and Zipcode {zipcode}</li>"
            list_of_surveys.append(survey)
        html_body = f"""<!DOCTYPE html>
                            <html>
                            <body>

                            <h1>Surveys for Covid-19</h1>

                                <ul>
                                    {str(list_of_surveys).replace(",", "")[1:-1]}
                                </ul>

                            <h1>Most Frequent Zipcodes for Surveys</h1>

                                <ul>
                                    {str(zipcode_list_html).replace(",", "")[1:-1]}
                                </ul>


                            </body>
                            </html> """.replace("'", "")
        print(html_body)
        return html_body