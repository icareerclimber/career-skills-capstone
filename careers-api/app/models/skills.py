from app.models import bp
from flask import request, jsonify
from random import shuffle
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
    if title not in pipeline.named_steps['nb'].classes_:
        return jsonify({'error': 'title not found in dataset', 'results': []})

    c = np.argwhere(pipeline.named_steps['nb'].classes_ == title)[0,0]
    print(c)
    print(max_features[c,:])
    return jsonify({'results': max_features[c,:].tolist()})

@bp.route('/titles', methods=['GET'])
def get_titles():
    return jsonify({'results': pipeline.named_steps['nb'].classes_.tolist()})

def load_models():
    global max_features
    global pipeline

    with open("/mnt/career-capstone/skills_model/20180725002822539809_pipeline_model.pkl", "rb") as f:
        pipeline = pickle.load(f)

    num_skills = 20
    max_feature_args = np.argsort(pipeline.named_steps['nb'].feature_log_prob_, 1)[:,-100:]
    sorted_features = np.array(pipeline.named_steps['tfidf'].get_feature_names())[max_feature_args]

    def clean_skills(sorted_features):
        accepted_skill_list = []
        for potential_skill in sorted_features:
            highest_match = len(potential_skill.split())
            for accepted_skill in accepted_skill_list:
                leftovers = list(set(potential_skill.split()) - set(accepted_skill.split()))
                if len(leftovers) < highest_match:
                    highest_match = len(leftovers)
            if highest_match > 1:
                accepted_skill_list.append(potential_skill)
        shuffle(accepted_skill_list)
        return accepted_skill_list[:num_skills]

    max_features = np.apply_along_axis(clean_skills, 1, sorted_features)

if __name__ == '__main__':
    print("Not meant to be run directly, start flask app to use")
else:
    load_models()
