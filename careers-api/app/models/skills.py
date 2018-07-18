from app.models import bp
from flask import request, jsonify
import pickle
import re, unicodedata
import nltk
import contractions
import numpy as np
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def preprocess_list(list_of_summaries):
    list_preprocessed_summary_text = []
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    for summary_text in list_of_summaries:
        summary_text = summary_text.lower()
        summary_text = re.sub(r'[^\w\s]', '', summary_text)
        summary_text = contractions.fix(summary_text)

        summary_tokens = nltk.word_tokenize(summary_text)
        summary_tokens = [word for word in summary_tokens if not word in stop_words]

        preprocessed_summary_tokens = []
        for token in summary_tokens:
            token = unicodedata.normalize('NFKD', token).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            if token[-2:] == 'ed' or token == 'wrote':
                token = lemmatizer.lemmatize(token,'v')
            if token[-1:] == 's':
                token = lemmatizer.lemmatize(token)
            preprocessed_summary_tokens.append(token)

        summary_text = ' '.join(preprocessed_summary_tokens)

        list_preprocessed_summary_text.append(summary_text)

    return list_preprocessed_summary_text

@bp.route('/similar_jobs', methods=['POST'])
def get_similarity():
    json = request.get_json()
    descriptions = [exp['description'] for exp in json['experience']]
    preprocesed_descriptions = preprocess_list(descriptions)
    vects = vectorizor.transform(preprocesed_descriptions)
    prediction = model.predict_proba(vects).reshape(-1,)
    sorted_predictions = sorted(zip(prediction, model.classes_), reverse=True)
    results = [{'title': c, 'probability': p} for p, c in sorted_predictions]
    return jsonify({'results': results})

@bp.route('/skills/<string:title>', methods=['GET'])
def get_skills(title):
    c = np.argwhere(model.classes_ == title)[0,0]
    print(c)
    print(max_features[c,:])
    return jsonify({'results': max_features[c,:].tolist()})

def load_models():
    global model
    global vectorizor
    global max_features
    global pipeline

    with open("./app/models/20180703161959266229_nb_model.pkl","rb") as f:
        model = pickle.load(f)
    with open("./app/models/20180703161959266229_tdidf_vect.pkl","rb") as f:
        vectorizor = pickle.load(f)

    num_skills = 10
    max_feature_args = np.argsort(model.feature_log_prob_, 1)[:,-num_skills:]
    max_features = np.array(vectorizor.get_feature_names())[max_feature_args]

if __name__ == '__main__':
    print("Not meant to be run directly, start flask app to use")
else:
    load_models()
