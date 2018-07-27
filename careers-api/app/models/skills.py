from app.models import bp
from flask import request, jsonify
import pickle
import numpy as np

@bp.route('/similar_jobs', methods=['POST'])
def get_similarity():
    json = request.get_json()
    descriptions = [exp['description'] for exp in json['experience']]
    prediction = pipeline.predict_proba(descriptions).reshape(-1,)
    sorted_predictions = sorted(zip(prediction, pipeline.named_steps['nb'].classes_), reverse=True)
    results = [{'title': c, 'probability': p} for p, c in sorted_predictions]
    return jsonify({'results': results})

@bp.route('/skills/<string:title>', methods=['GET'])
def get_skills(title):
    c = np.argwhere(pipeline.named_steps['nb'].classes_ == title)[0,0]
    print(c)
    print(max_features[c,:])
    return jsonify({'results': max_features[c,:].tolist()})

def load_models():
    global max_features
    global pipeline

    with open("/mnt/career-capstone/skills_model/20180725002822539809_pipeline_model.pkl", "rb") as f:
        pipeline = pickle.load(f)

    num_skills = 10
    max_feature_args = np.argsort(pipeline.named_steps['nb'].feature_log_prob_, 1)[:,-num_skills:]
    max_features = np.array(pipeline.named_steps['tfidf'].get_feature_names())[max_feature_args]

if __name__ == '__main__':
    print("Not meant to be run directly, start flask app to use")
else:
    load_models()
