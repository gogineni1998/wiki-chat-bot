from transformers import pipeline

from flask import Flask, request



summarizer = pipeline("summarization")

app = Flask(__name__)


@app.route('/',methods = ['POST'])
def summary_generator():
    text = request.get_json()
    new_text = [text['input']]
    summary = summarizer(new_text, max_length=100, min_length=10, length_penalty=2.0, num_beams=4)[0]['summary_text']


if __name__ == '__main__':
   app.run(host="0.0.0.0")
