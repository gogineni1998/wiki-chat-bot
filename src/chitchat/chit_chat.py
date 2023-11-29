from flask import Flask, request
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

mname = "facebook/blenderbot-400M-distill"
model = BlenderbotForConditionalGeneration.from_pretrained(mname)
tokenizer = BlenderbotTokenizer.from_pretrained(mname)


app = Flask(__name__)


@app.route('/',methods = ['POST'])
def generate_response():
    text = request.get_json()
    new_text = [text['input']]
    UTTERANCE = new_text
    inputs = tokenizer([UTTERANCE], return_tensors="pt")
    reply_ids = model.generate(**inputs)
    result = tokenizer.batch_decode(reply_ids)[0].replace('/','')
    result = result.replace('<s>','')
    return result




if __name__ == '__main__':
   app.run(host="0.0.0.0")