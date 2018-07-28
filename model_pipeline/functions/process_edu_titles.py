import pandas as pd
import re
from nltk import word_tokenize


def get_list_small_words(list_of_titles, word_size):
    # Create a list of acronyms by selecting all words that are `word_size` or less letters
    word_list = []
    for row in list_of_titles:
        [word_list.append(x) for x in row if len(x) < word_size]
    return list(set(word_list))



def load_dict(filename):
    # Read file to dictionary
    return pd.read_csv(filename, encoding='latin-1')[['keyword','type']].set_index('keyword')['type'].to_dict()



def split_to_subject_degree(list_of_titles, word_list):
    # Iterate through all the degree titles. Process each word:
    # 1. If the word = 'in', then add it as a `degree_row`, remove that word from the 
    #   `subject_row`, and stop processing word
    # 2. If the word is in the acronym list or the manual dictionary, then add it as a
    #    `degree_row`, remove that word from the `subject_row`, and stop processing word
    # 3. If the word is not 1 or 2, stop processing the word

    # Load these dictionaries from the `configuration_files` folder
    degree_type_word_dict = load_dict('functions/configuration_files/degree_type_word_dict.csv')
    degree_type_phrase_dict = load_dict('functions/configuration_files/degree_type_phrase_dict.csv')

    degree_name_list = []
    subject_name_list = []
    for row in list_of_titles:
        degree_row = []
        subject_row = row
        for token in row:
            if token == 'in':
                degree_row.append(token)
                subject_row = subject_row[1:]
                break
            elif token in list(degree_type_word_dict.keys()) + word_list:
                degree_row.append(token)
                subject_row = subject_row[1:]
            else:
                break
        degree_name_list.append(' '.join(degree_row))
        subject_name_list.append(' '.join(subject_row))
    return degree_name_list, subject_name_list



def tag_with_degree_category(list_of_degrees, list_of_subjects):
    # This function takes the list of degrees and tags each degree with one or more degree categories
    last_dict = {
        'immersive':'bootcamp',
        'certificate':'bootcamp',
        'bootcamp':'bootcamp',
        'boot camp':'bootcamp',
        'license':'license',
        'licensure':'license',
        'certification':'certificate',
        'certificate':'certificate',
        }

    degree_category_list = []

    # Load these dictionaries from the `configuration_files` folder
    degree_type_word_dict = load_dict('functions/configuration_files/degree_type_word_dict.csv')
    degree_type_phrase_dict = load_dict('functions/configuration_files/degree_type_phrase_dict.csv')

    # Iterate through each degree 
    for index, row in enumerate(list_of_degrees):

        degree_category = []
        found_key=0

        # First, use the `degree_type_word_dict` dictionary to assign a degree category
        for key in filter(lambda x: str(degree_type_word_dict[x])!='nan', degree_type_word_dict):
            if key in row.split():
                degree_category.append(degree_type_word_dict[key])
                found_key=1

        if found_key==0:
            # If degree category is still empty,
            # use the `degree_type_phrase_dict` dictionary to assign a degree category
            for phrase in degree_type_phrase_dict:
                if re.match(phrase,row):
                    degree_category.append(degree_type_phrase_dict[phrase])
                    found_key=1

        if found_key==0:
            # If degree category is still empty,
            # use the `last_dict` dictionary and match on the subject instead of the degree
            # to assign a degree category
            for key in last_dict:
                if key in list_of_subjects[index]:
                    degree_category.append(last_dict[key])

        degree_category_list.append(list(set([x.strip() for x in degree_category if str(x)!='nan' and str(x)!= ' '])))

    return degree_category_list



def find_best_degree_category(list_of_degree_categories):
    # This function takes a list of degree categories and returns the highest ranked one
    # The `degree_category_ranking` list shows ranking of the categories
    # Each row will be assigned only 1 degree category in the end
    degree_category_ranking = ['minor',
                'all but dissertation',
                'juris doctor',
                'doctorate',
                'associates',
                'some education',
                'masters',
                'bachelors',
                'license',
                'hs diploma',
                'vocational',
                'certificate']

    final_degree_category_list = []
    for row in list_of_degree_categories:
        if len(row) > 1:
            for job in degree_category_ranking:
                if job in row:
                    final_degree_category_list.append(job)
                    break
        elif len(row) == 1:
            final_degree_category_list.append(row[0])
        else:
            final_degree_category_list.append('unknown')

    return final_degree_category_list



def process_edu_titles(list_of_titles):

    # Remove anything outside of words and numbers
    list_of_titles = [re.sub('[^A-Za-z0-9\s]+', '', row.lower()) for row in list_of_titles]
    
    # Tokenize all the words
    list_of_titles = [word_tokenize(row) for row in list_of_titles]

    # Find all the acronyms in the education titles
    acronym_list = get_list_small_words(list_of_titles, 5)

    # Split the overall title into subject and degree
    degree_name_list, subject_name_list = split_to_subject_degree(list_of_titles, acronym_list)

    # Find the degree categories for each degree
    degree_category_list = tag_with_degree_category(degree_name_list, subject_name_list)
    
    # Condense the degree categories into one degree
    final_degree_category_list = find_best_degree_category(degree_category_list)
    
    # Return these lists
    return subject_name_list, degree_name_list, final_degree_category_list
