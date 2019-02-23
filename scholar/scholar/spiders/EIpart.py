from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

browser = webdriver.Chrome()
def sele_ei(titles):
    papers = []
    for title in titles:
        browser.get('https://www.engineeringvillage.com/search/quick.url')
        input = browser.find_element_by_id('search-word-1')
        input.send_keys(title)
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='abstractlink']")))
        link = browser.find_element_by_xpath("//a[@class='abstractlink']").get_attribute('href')
        print('link:'+link)
        browser.get(link)
        wait.until(EC.presence_of_element_located((By.ID, 'abstractWrappper')))
        details = {}

sele_ei(['Recognizing clinical entities in hospital discharge summaries using Structural Support Vector Machines with word representation features',
         'Prediction of protein binding sites in protein structures using hidden Markov support vector machine'])