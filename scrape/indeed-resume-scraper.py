#!/usr/bin/python

import sys
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
import time
import requests
import random
import pandas as pd
import boto3
import botocore
import logging
from datetime import date, datetime, timedelta
import traceback
import csv



# Process one city at a time. In order to do so,
# get a distinct list of the resume ids for that city.
# Update the variables below for the city name.
city_name = "nyc"
resume_id_list = city_name + "_resume_ids.csv"
out_file_name = city_name + "_resume_data.csv"

def main():
    logging.basicConfig(filename="indeed-resume-scraper.log", level=logging.INFO)

    with open(resume_id_list, 'rb') as f:
        reader = csv.reader(f)
        resume_ids = list(reader)

    for resume_id in resume_ids:
        resume_id = resume_id[0]
        sleep_non_bot()
        job_link_url = "https://www.indeed.com/r/{}".format(resume_id)
        print(job_link_url)
        logging.info("Scraping Job URL:{}".format(job_link_url))

        try:
            job_link_page = requests.get(job_link_url)
            job_link_soup = BeautifulSoup(job_link_page.text, "html.parser")
            basic_info = job_link_soup.find(name="div", attrs={"id":"basic_info_cell"})
            containers = job_link_soup.findAll(name="div", attrs={"class":"items-container"})
            combined_list = []
            combined_list.append(basic_info)
            [combined_list.append(x) for x in containers]
            with open(out_file_name, 'a') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                for row in combined_list:
                    wr.writerow([resume_id,row])

        except Exception as e:
            logging.error("Failed to scrape for resume id:{}".format(job_link_url))
            print(traceback.format_exc())
            continue


def log(msg):
    print(msg)
    logging.info(msg)


def sleep_non_bot():
    sleep_time = random.randint(1100,2300)/1000.0
    #print("Sleeping for time={} seconds".format(str(sleep_time)))
    logging.info("Sleeping for time={} seconds".format(str(sleep_time)))
    time.sleep(sleep_time) #waits for a random time so that the website don't consider you as a bot


# Usage: python indeed-scraper.py <search-term>
if __name__ == "__main__":
    main()
