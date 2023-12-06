import pickle

from flask import Flask, request

lr = pickle.load(open('logistic_regression.pkl', 'rb'))
nb = pickle.load(open('naive_bayes.pkl', 'rb'))

app = Flask(__name__)

@app.route('/',methods = ['POST'])
def hello_world():
    text = request.get_json()
    new_text = [text['input']]

    # Logistic Regression
    lr_new_text_processed = lr.named_steps['vect'].transform(new_text)
    lr_new_text_tfidf = lr.named_steps['tfidf'].transform(lr_new_text_processed)
    lr_predicted_class = lr.named_steps['clf'].predict(lr_new_text_tfidf)
    lr_predicted_probabilities = lr.named_steps['clf'].predict_proba(lr_new_text_tfidf)
    lr_class_names = lr.named_steps['clf'].classes_

    # Naive Bayes
    nb_new_text_processed = nb.named_steps['vect'].transform(new_text)
    nb_new_text_tfidf = nb.named_steps['tfidf'].transform(nb_new_text_processed)
    nb_predicted_class = nb.named_steps['clf'].predict(nb_new_text_tfidf)
    nb_predicted_probabilities = nb.named_steps['clf'].predict_proba(nb_new_text_tfidf)
    nb_class_names = nb.named_steps['clf'].classes_

    print(lr_class_names, lr_predicted_probabilities[0])
    print(nb_class_names, nb_predicted_probabilities[0])

    max_probability = -1
    temp_topic = "Chitchat"
    main_topic = "Chitchat"
    for i in range(0,len(lr_class_names)):
        avg_prob = (lr_predicted_probabilities[0][i] + nb_predicted_probabilities[0][i]) / 2
        if(max_probability < lr_predicted_probabilities[0][i]):
            max_probability = lr_predicted_probabilities[0][i]
            temp_topic = lr_class_names[i]
    if(max_probability > 0.2):
        main_topic = temp_topic
    return main_topic


if __name__ == '__main__':
   app.run(host="0.0.0.0")
