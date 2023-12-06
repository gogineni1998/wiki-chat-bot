from flask import Flask, request
from flask_cors import cross_origin
from flask import jsonify
import requests
import json
app = Flask(__name__)


@app.route('/',methods = ['POST'])
@cross_origin(supports_credentials=True)
def start_generation():
    ip_address = json.load(open('utils/utils.json'))
    text = request.get_json()
    new_text = text['input']
    url = "http://"+ip_address['Classifier']+":5000"
    data = {"input": new_text}
    class_type = requests.post(url, json = data)
    print(class_type.text)
    url = "http://"+ip_address[class_type.text]+":5000"
    print(url)
    if(class_type.text == 'Chitchat'):
        chit_chat_response = requests.post(url, json = data)
        return jsonify({"data":chit_chat_response.text})
    
    docs_data = requests.post(url, json = data)
    data = {"input": docs_data.text}
    url = "http://"+ip_address['Summarizer']+":5000"
    summarized_data = requests.post(url, json = data)
    return jsonify({"data":summarized_data.text})



if __name__ == '__main__':
   app.run(host="0.0.0.0")

