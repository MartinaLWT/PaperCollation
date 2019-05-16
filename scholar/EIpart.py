from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import re
from scholar import google_settings


def get_ei_info(title):
    paper_list = []
    setting_1 = google_settings.Settings()
    browser = setting_1.browser
    wait = WebDriverWait(browser, 20)
    browser.get('https://www.engineeringvillage.com/search/quick.url')
    wait.until(EC.presence_of_element_located((By.ID, "sect1")))
    browser.find_element_by_id("sect1").find_elements_by_tag_name("option")[5].click()
    input = browser.find_element_by_id('search-word-1')
    input.send_keys(title)
    input.send_keys(Keys.ENTER)
    details = {"title": title}
    wait.until(EC.presence_of_element_located((By.ID, "query-bar")))
    article_list = browser.find_elements_by_xpath("//div[@class='row result-row']")
    for i in range(0, len(article_list)):
        title_found = browser.find_element_by_xpath("//div[@id='result_{}']/div/div/div/div/div/h3/a[@class='abstractlink']".format(str(i))).get_attribute('text')
        if title.lower() == title_found.lower():
            link = browser.find_element_by_xpath("//div[@id='result_{}']/div/div/div/div/div/h3/a[@class='abstractlink']".format(str(i))).get_attribute('href')
            for j in range(0, 2):
                try:
                    browser.get(link)
                    wait.until(EC.presence_of_element_located((By.ID, 'abstractWrappper')))
                    browser.find_element_by_id("detailedTabLink").click()
                    wait.until(EC.presence_of_element_located((By.ID, 'abstractWrappper')))
                    break
                except:
                    pass
            #文章题目
            details['title'] = title_found
            author_http = browser.find_elements_by_xpath("//span[@class='abs_authors']/a")
            #作者列表
            details['Author'] = [y for y in [x.get_attribute('text') for x in author_http] if y != ""]
            #出版年份
            try:
                publication_year = browser.find_element_by_xpath("//div[@class='abs_head_pad'][contains(.,'Issue date')]").get_attribute('textContent')
                details['Published date'] = re.sub('[\r\t\nPublication Year:]', '', publication_year)
            except:
                details['Published date'] = None
            #出版刊物
            try:
                source_title = browser.find_element_by_xpath("//span[@class='abs_headers'][contains(text(),'Source title')]/../div").get_attribute('textContent')
                details['Publication'] = source_title
            except:
                details['Publication'] = None
            #引用他人
            try:
                reference = browser.find_element_by_xpath("//div[@class='abs_head_pad'][contains(.,'Number of references')]").get_attribute('textContent')
                details['Reference'] = re.sub('[\r\n\tNumber of references:]', '', reference)
            except:
                details['Reference'] = None
            #被引用
            try:
                citations = browser.find_element_by_xpath("//div[@class='pps-col plx-citation']/div/ul/li/span[2]").get_attribute('textContent')
                details['Citations'] = citations
            except:
                details['Citations'] = None
            #文章类型
            try:
                document = browser.find_element_by_xpath("//div[@class='abs_head_pad'][contains(.,'Document type')]").get_attribute('textContent')
                details['Document type'] = re.sub('[\r\n\tDocument type:]', '', document)
            except:
                details['Document type'] = None
            #DOI
            try:
                DOI = browser.find_element_by_xpath("//div[@class='abs_head_pad'][contains(.,'DOI')]").get_attribute('textContent')
                details['DOI'] = re.sub('[\r\n\tDOI::]', '', DOI)
            except:
                details['DOI'] = None
            print(details)
            browser.close()
            return details
    details["tag"] = "Not Found"
    browser.close()
    return paper_list

get_ei_info('Prediction of protein binding sites in protein structures using hidden Markov support vector machine')
#         'Clinical entity recognition using structural support vector machines with rich features')

