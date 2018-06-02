Resume Scraping

Scraping Indeed resumes takes 2 functions.

1. 
Run the `indeed-id-scraper.py` function. You need to change the inside of the function to point to the relevant city and radius (from the city). This function will find all the resume_id records for the job titles listed in `jobtitles.txt` for every city. It will scrape 1000 records for each job title/city combination. 

2. After you have collected the resume_ids, take the distinct list of resume_ids and run the `indeed-resume-scraper.py` function. This function will save the content of each resume into a csv file. I recommend doing smaller subsets and giving the files distinct names. 
