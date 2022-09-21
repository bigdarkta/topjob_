from bs4 import BeautifulSoup
import requests
from random import random
from time import sleep
import csv
import re

def generate_url(country_code, country):

    if country == "España":
        url = "https://es.indeed.com/jobs?q=data%20scientist&l=Espa%C3%B1a"
        return url

    elif country == "Unided Kingdom":
        url = "https://uk.indeed.com/jobs?q=data%20scientist&l=United%20Kingdom&vjk=96e2e177ebcda5a6"
        return url

    else: 
        url_template = "https://{}.indeed.com/jobs?q=data%20scientist&l={}"
        url = url_template.format(country_code, country)
        return url

    return url

def save_record_to_csv(record, filepath, create_new_file=False):
    """Save an individual record to file; set `new_file` flag to `True` to generate new file"""
    header = ["job_title", "company", "location", "job_summary", "post_date", "more_info", "salary", "job_url"]
    if create_new_file:
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
    else:
        with open(filepath, mode='a+', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(record)

def collect_job_cards_from_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('div', 'job_seen_beacon')

    return cards, soup


def sleep_for_random_interval():
    seconds = random() * 10
    sleep(seconds)


def request_jobs_from_indeed(url):

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                        'AppleWebKit/537.11 (KHTML, like Gecko) '
                        'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def find_next_page(country, country_code, i):
    if country == "España":
        country = "Espa%C3%B1a"
    if country == "United Kingdom":
        country = "United%20Kingdom"
    try: 
        base = "https://{}.indeed.com"
        base_url = base.format(country_code)
        pattern = "/jobs?q=data+scientist&l={}&start={}0"
        pattern_url = pattern.format(country, i)

        new_url = base_url + pattern_url

        return new_url
    except AttributeError:
        return None


def extract_job_card_data(card):
    atag = card.h2.a
    try:
        job_title = card.find("h2", "jobTitle").text.strip()
    except AttributeError:
        job_title = ''
    try:
        company = card.find('span', 'companyName').text.strip()
    except AttributeError:
        company = ''
    try:
        location = card.find('div', 'companyLocation').text.strip()
    except AttributeError:
        location = ''
    try:
        job_summary = card.find('div', 'job-snippet').text.strip()
    except AttributeError:
        job_summary = ''
    try:
        post_date = card.find('span', 'date').text.strip()
    except AttributeError:
        post_date = ''

    try:
        more_info = card.find('div', "attribute_snippet").text.strip()
    except AttributeError:
        more_info = ''
    try:
        salary = card.find('div', 'salary-snippet-container').text.strip()
    except AttributeError:
        salary = ''
        
    job_url = 'https://www.indeed.com' + atag.get('href')
    return job_title, company, location, job_summary, post_date, more_info, salary, job_url


def main(country_code, country, filepath, pages):
    unique_jobs = set()  # track job urls to avoid collecting duplicate records
    print("Starting to scrape indeed for")
    url = generate_url(country_code, country)
    save_record_to_csv(None, filepath, create_new_file=True)
    i = 10

    while True:
        if i > pages:
            break
        print(f"Scrapping page_{i}...{url}")
        html = request_jobs_from_indeed(url)
        if not html:
            break
        cards, soup = collect_job_cards_from_page(html)
        for card in cards:
            record = extract_job_card_data(card)
            if not record[-1] in unique_jobs:
                save_record_to_csv(record, filepath)
                unique_jobs.add(record[-1])
        sleep_for_random_interval()
        url = find_next_page(country, country_code, i)
        i += 1
        print('Finished collecting {:,d} job postings.'.format(len(unique_jobs)))
    print('Finished collecting {:,d} job postings.'.format(len(unique_jobs)))

if __name__ == '__main__':
    # job search settings
    country_code = "uk"
    country = "United Kingdom"
    pages = 15

    # <<<<< change --> yourPATH >>>>>
    path = f'/Users/irena/Desktop/scraper/indeed-scraper/scrapperIndeed/output_data/data_scientist_jobs_{country}.csv'

    main(country_code, country, path, pages)