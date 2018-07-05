import pandas as pd
import matplotlib.pyplot as plt
import re


# This function moves qualifiers from job title list to experience list
def parse_experience(list_of_jobs):

    # Job qualifiers that will be moved to experience list
    qualifiers = [
        'vice_president','president','principal','senior','junior','lead',
        'entry','mid','intern','1','2','3','4','5','6','7',
                    ]

    clean_job_list = []
    experience_list = []

    for job in list_of_jobs:
        single_job_experience = []
        single_job_title = []
        for job_word in [c.strip() for c in re.split('(\W+)', job) if c.strip() != '']:
            if job_word in qualifiers:
                single_job_experience.append(job_word)
            else:
                single_job_title.append(job_word)
        clean_job_list.append(' '.join(single_job_title))
        experience_list.append(single_job_experience)
    return clean_job_list, experience_list

def trash_words(list_of_jobs):

    # Words that will be removed from job title
    trash_words_list = ['jc', 'mts', 'level']
    cleaned_list_of_jobs = []
    for job in list_of_jobs:
        job_tokens = [c.strip() for c in re.split('(\W+)', job) if c.strip() != '']
        job = [job_word for job_word in job_tokens if job_word not in trash_words_list]
        cleaned_list_of_jobs.append(' '.join(job))
    return cleaned_list_of_jobs
        
def remove_special_characters(char_list, list_of_jobs):
    # This will remove characters from variable char_list
    for char in char_list:
        list_of_jobs = [job.replace(char,' ') for job in list_of_jobs]
    return list_of_jobs

def manual_update_words(list_of_jobs):

    # Words that will be manually changed
    manual_update_word_dict = pd.read_csv('functions/configuration_files/manual_update_word_dict.csv', encoding='latin-1')
    manual_update_word_dict = manual_update_word_dict[~manual_update_word_dict.new_word.isnull()]\
                                [['original_word','new_word']]\
                                .set_index('original_word')['new_word']\
                                .to_dict()
    cleaned_list_of_jobs = []
    for job in list_of_jobs:
        job_tokens = [c.strip() for c in re.split('(\W+)', job) if c.strip() != '']
        job = [manual_update_word_dict[job_word] if job_word in manual_update_word_dict 
                    else job_word 
                    for job_word in job_tokens]
        cleaned_list_of_jobs.append(' '.join(job))
    return cleaned_list_of_jobs

def manual_update_job_titles(list_of_jobs):
    # Manual transformations of similar jobs
    manual_update_job_dict = pd.read_csv('functions/configuration_files/manual_update_job_dict.csv', encoding='latin-1')
    manual_update_job_dict = manual_update_job_dict[~manual_update_job_dict.new_job.isnull()]\
                            [['original_job','new_job']]\
                            .set_index('original_job')['new_job']\
                            .to_dict()
    cleaned_list_of_jobs = []
    for job in list_of_jobs:
        if job in manual_update_job_dict:
            job = manual_update_job_dict[job]
        cleaned_list_of_jobs.append(job)
    return cleaned_list_of_jobs

def remove_words_in_parenthesis(list_of_jobs):
    # This will remove all the values inside parentheses
    cleaned_list_of_jobs = []
    for job in list_of_jobs:
        job = re.sub(re.compile("\((.*?)\)"), '', job)
        job = re.sub(re.compile("\[(.*?)\]"), '', job)
        cleaned_list_of_jobs.append(job)
    return cleaned_list_of_jobs

def remove_words_after_special_char(char_list, list_of_jobs):
    # This will remove the text after the character in char_list
    for char in char_list:
        list_of_jobs = [job.split(char, -1)[0] for job in list_of_jobs]
    return list_of_jobs

def get_forward_slash_longest_section(special_char, list_of_jobs):
    # For strings with /, split by / and take the longest string
    cleaned_list_of_jobs = []
    for job in list_of_jobs:
        if special_char in job:
            split_lengths = [len(x.split()) for x in job.split(special_char)]
            job = job.split(special_char)[split_lengths.index(max(split_lengths))]
        cleaned_list_of_jobs.append(job)
    return cleaned_list_of_jobs

def remove_lead_trail_special_char(list_of_jobs):
    cleaned_list_of_jobs = []
    for job in list_of_jobs:
        job = re.sub(r"^\W+", "", job)
        job = re.sub(r"\W*?$", "", job)
        cleaned_list_of_jobs.append(job)
    return cleaned_list_of_jobs

def clean_job(list_of_jobs):
    
    # Lowercase and strip whitespaces
    clean_job_list = [job.strip().lower() for job in list_of_jobs]

    # Replace ,, with ,
    clean_job_list = [job.replace(',,',',') for job in clean_job_list]

    # Remove .
    clean_job_list = [job.replace('.','') for job in clean_job_list]

    # Special logic replacements
    clean_job_list = [job.replace(' & ',' and ') for job in clean_job_list]
    clean_job_list = [job.replace('vice president','vice_president') for job in clean_job_list]
    clean_job_list = [job.replace('vice-president','vice_president') for job in clean_job_list]
    clean_job_list = [job.replace('wi-fi','wifi') for job in clean_job_list]
    clean_job_list = [job.replace("ass't",'assistant') for job in clean_job_list]

    # Replace special characters with space
    clean_job_list = remove_special_characters( [':',';','#',"'"] , clean_job_list)
    
    # Remove specific words
    clean_job_list = trash_words(clean_job_list)

    # Manually update words using list
    clean_job_list = manual_update_words(clean_job_list)

    # First round pull out qualifiers
    clean_job_list, experience_list1 = parse_experience(clean_job_list)

    # Delete all content between parenthesis (...) or [...]
    clean_job_list = remove_words_in_parenthesis(clean_job_list)

    # For strings with special characters / and -, split by special character and take the longest string
    clean_job_list = get_forward_slash_longest_section('/',clean_job_list)
    clean_job_list = get_forward_slash_longest_section(' - ',clean_job_list)
    clean_job_list = get_forward_slash_longest_section('- ',clean_job_list)
    clean_job_list = get_forward_slash_longest_section(' -',clean_job_list)

    # Remove leading or trailing special characters
    clean_job_lit = remove_lead_trail_special_char(clean_job_list)

    # Remove all text after - and (
    clean_job_list = remove_words_after_special_char(['(',')','[',']'], clean_job_list)

    # Replace - with ' '
    clean_job_list = [job.replace('-',' ') for job in clean_job_list]

    # Replace ,, with ,
    clean_job_list = [job.replace(',,',',') for job in clean_job_list]
    clean_job_list = [job.replace(', ,',',') for job in clean_job_list]
    clean_job_list = [job.replace(',  ,',',') for job in clean_job_list]

    # For strings with comma, reverse the order and remove comma
    clean_job_list = [job.split(',', 1)[1].strip() + ' ' + job.split(',', 1)[0].strip() 
                      if len(job.split(',', 1))>1 else job
                      for job in clean_job_list]
    
    # If there is more than 1 comma, remove the text for the 2nd
    clean_job_list = remove_words_after_special_char([','], clean_job_list)
    
    # Manually update job titles using list
    clean_job_list = manual_update_job_titles(clean_job_list)

    # Second round pull out qualifiers
    clean_job_list, experience_list2 = parse_experience(clean_job_list)
    
    # Clean up extra whitespaces
    clean_job_list = [job.replace('  ',' ').strip() for job in clean_job_list]
    
    # Remove any numbers
    clean_job_list = [x for x in clean_job_list if not isinstance(x, int)]

    # Merge the 2 rounds of qualifier grabbing
    experience_list = list(map(list.__add__, experience_list1, experience_list2))

    # Clean job of leading or trailing special characters
    clean_job_lit = remove_lead_trail_special_char(clean_job_list)

    # Sort the experience list
    sorted_experience_list = []
    for item in experience_list:
        sorted_experience_list.append(sorted(set(item)))

    return list_of_jobs, clean_job_list, sorted_experience_list
