import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

def get_all_urls():

    urls = []

    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1120, 1000)
    url = "https://www.glassdoor.ca/Job/canada-cyber-security-jobs-SRCH_IL.0,6_IN3_KO7,21.htm?"
    driver.get(url)

    for i in range (5):
        time.sleep(2)
        button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/section/article/div[2]/div/div[1]/button[7]')
        driver.execute_script("arguments[0].click();", button)
        #driver.switch_to.window(driver.window_handles[1])
        new_url = driver.current_url
        urls.append(new_url)
        #print("URL after click button --->", new_url)
        #print("new_url-------->", new_url)
        time.sleep(2)
        """
        company_name = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/section/div/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]').text
        print("company name ----->", company_name)
        time.sleep(2)
        """

    return urls
    
"""
urls = get_all_urls()
for url in urls:
    print(url)
"""
