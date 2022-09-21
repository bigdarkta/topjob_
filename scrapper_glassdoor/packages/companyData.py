# Import necessary libraries
# standard libraries
import re
from time import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

def extract_companyLocationNoSalary(url):

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    driver.implicitly_wait(3)
    
    button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/header/div/div/div[2]')
    button.click()
    company_loc = driver.find_element(By.XPATH, '//*[@id="headquarters"]').text
    company_size = driver.find_element(By.XPATH, '//*[@id="size"]').text

    return (company_loc, company_size)

def extract_companyLocationSalary(url):

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    driver.implicitly_wait(3)
    
    button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/header/div/div/div[3]')
    button.click()
    company_loc = driver.find_element(By.XPATH, '//*[@id="headquarters"]').text
    company_size = driver.find_element(By.XPATH, '//*[@id="size"]').text

    return (company_loc, company_size)