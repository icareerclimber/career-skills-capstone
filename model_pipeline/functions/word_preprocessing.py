import contractions
import nltk
import re
import unicodedata
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def preprocess_list(list_of_summaries):
    list_preprocessed_summary_text = []
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    for summary_text in list_of_summaries:
        summary_text = summary_text.lower()
        summary_text = summary_text.replace('amp;amp;','')
        summary_text = summary_text.replace('-','')
        summary_text = re.sub(r'[^A-Za-z0-9&\-]+', ' ', summary_text)
        summary_text = contractions.fix(summary_text)
        
        summary_tokens = summary_text.split(' ')
        summary_tokens = [word for word in summary_tokens if not word in stop_words]

        preprocessed_summary_tokens = []
        for token in summary_tokens:
            token = unicodedata.normalize('NFKD', token).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            if token.isdigit():
                continue
            if token[-2:] == 'ed' or token == 'wrote':
                token = lemmatizer.lemmatize(token,'v')
            if token[-1:] == 's':
                token = lemmatizer.lemmatize(token)
            preprocessed_summary_tokens.append(token)
            
        summary_text = ' '.join(preprocessed_summary_tokens)
        
        list_preprocessed_summary_text.append(summary_text)

    return list_preprocessed_summary_text
