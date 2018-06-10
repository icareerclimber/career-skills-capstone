#!/usr/bin/python
import logging
import csv
import re
import sys

# create logger
logger = logging.getLogger("extract_experience")
logger.setLevel(logging.INFO)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

def main(input_file, output_file):
    with open(input_file, 'r') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_ALL)
        
        for job in reader:
            logger.info("Processing job: {}".format(job[0]))
            matches = re.findall("(\d+).? (years|yrs)", job[-1])

            experience = [int(exp[0]) for exp in matches]
            max_exp = None
            if len(experience) > 0:
                max_exp = max(experience)
            logger.info(max_exp)
            job.append(max_exp)
            with open(output_file, 'a') as o:
                writer = csv.writer(o, quoting=csv.QUOTE_ALL)
                writer.writerow(job)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])