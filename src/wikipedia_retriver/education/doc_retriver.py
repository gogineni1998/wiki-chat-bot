import json
import pickle
from sentence_transformers import SentenceTransformer, util

from flask import Flask, request

app = Flask(__name__)

model = SentenceTransformer('clips/mfaq')

file = open('Education.pkl', 'rb')
data = pickle.load(file)


@app.route('/',methods = ['POST'])
def retrive_docs():
    text = request.get_json()
    new_text = [text['input']]
    query_embedding = model.encode(new_text)
    results = util.semantic_search(query_embedding, data,top_k=2)
    json_file = open('Education.json','rb')
    education_data = json.load(json_file)
    document = ""
    for result in results[0]:
        document = document + education_data[result['corpus_id']]['summary']
    return document

if __name__ == '__main__':
   app.run(host="0.0.0.0")