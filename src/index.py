from flask import Flask, request
from flask_cors import cross_origin
from flask import jsonify
import requests
import json
app = Flask(__name__)


analytics = {}
analytics["Health"] = 0
analytics["Environment"] = 1
analytics["Technology"] = 2
analytics["Economy"] = 3
analytics["Entertainment"] = 4
analytics["Sports"] = 5
analytics["Politics"] = 6
analytics["Education"] = 7
analytics["Travel"] = 8
analytics["Food"] = 9
analytics["Chitchat"] = 10

analytics_count = [0,0,0,0,0,0,0,0,0,0,0]

@app.route('/',methods = ['POST'])
@cross_origin(supports_credentials=True)
def start_generation():
    ip_address = json.load(open('utils/utils.json'))
    text = request.get_json()
    new_text = text['input'].lower()
    topics = text['topics']
    url = "http://"+ip_address['Classifier']+":5000"
    data = {"input": new_text,
    "topics_selected" : topics}
    class_type = requests.post(url, json = data)
    print(class_type.text)
    url = "http://"+ip_address[class_type.text]+":5000"
    print(url)
    if(class_type.text == 'Chitchat'):
        analytics_count[analytics[class_type.text]] = analytics_count[analytics[class_type.text]] + 1
        chit_chat_response = requests.post(url, json = data)
        return jsonify({"data":chit_chat_response.text,"topic" : class_type.text,"analytics" : analytics_count})

    analytics_count[analytics[class_type.text]] = analytics_count[analytics[class_type.text]] + 1
    docs_data = requests.post(url, json = data)
    data = {"input": docs_data.text}
    url = "http://"+ip_address['Summarizer']+":5000"
    summarized_data = requests.post(url, json = data)
    return jsonify({"data":summarized_data.text,"topic" : class_type.text,"analytics" : analytics_count})

@app.route('/analytics',methods = ['GET'])
@cross_origin(supports_credentials=True)
def get_analytics():
    return {"analytics" : analytics_count}



if __name__ == '__main__':
   app.run(host="0.0.0.0")

