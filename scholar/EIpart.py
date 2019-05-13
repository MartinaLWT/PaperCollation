from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import scholar.settings as settings
import re


executable_path = settings.executable_path


chrome_options = webdriver.ChromeOptions()
pref = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", pref)
browser = webdriver.Chrome(executable_path, chrome_options=chrome_options)
browser.implicitly_wait(10)


def get_ei_info(titles):
    paper_list = []
    for title in titles:
        wait = WebDriverWait(browser, 10)
        browser.get('https://www.engineeringvillage.com/search/quick.url')
        wait.until(EC.presence_of_element_located((By.ID, "sect1")))
        browser.find_element_by_id("sect1").find_elements_by_tag_name("option")[5].click()
        input = browser.find_element_by_id('search-word-1')
        input.send_keys(title)
        input.send_keys(Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.ID, "query-bar")))

        article_list = browser.find_elements_by_xpath("//div[@class='row result-row']")
        for i in range(len(article_list)):
            title_found = browser.find_element_by_xpath("//div[@id='result_{}']/div/div/div/div/div/h3/a[@class='abstractlink']".format(str(i))).get_attribute('text')
            if title.lower() == title_found.lower():
                link = browser.find_element_by_xpath("//div[@id='result_{}']/div/div/div/div/div/h3/a[@class='abstractlink']".format(str(i))).get_attribute('href')
                browser.get(link)
                wait.until(EC.presence_of_element_located((By.ID, 'abstractWrappper')))
                browser.find_element_by_id("detailedTabLink").click()
                wait.until(EC.presence_of_element_located((By.ID, 'abstractWrappper')))
                details = {}
                #文章题目
                details['title'] = title_found
                author_http = browser.find_elements_by_xpath("//span[@class='abs_authors']/a")
                #作者列表
                details['Author'] = [y for y in [x.get_attribute('text') for x in author_http] if y != ""]
                #出版年份
                publication_year = browser.find_element_by_xpath("//div[@class='abs_head_pad'][contains(.,'Publication Year')]").get_attribute('textContent')
                details['Published date'] = re.sub('[\r\t\nPublication Year:]', '', publication_year)
                #出版刊物
                source_title = browser.find_element_by_xpath("//span[@class='abs_headers'][contains(text(),'Source title')]/../div").get_attribute('textContent')
                details['Publication'] = source_title
                #引用
                reference = browser.find_element_by_xpath("//div[@class='abs_head_pad'][contains(.,'Number of references')]").get_attribute('textContent')
                details['Reference'] = re.sub('[\r\n\tNumber of references:]', '', reference)
                #文章类型
                document = browser.find_element_by_xpath("//div[@class='abs_head_pad'][contains(.,'Document type')]").get_attribute('textContent')
                details['Document type'] = re.sub('[\r\n\tDocument type:]', '', document)
                #DOI
                DOI = browser.find_element_by_xpath("//div[@class='abs_head_pad'][contains(.,'DOI')]").get_attribute('textContent')
                details['DOI'] = re.sub('[\r\n\tDOI::]', '', DOI)
                paper_list.append(details)
                break
    print(paper_list)

#传入姓名与论文title的列表进行ei上的爬取
#sele_ei(['Prediction of protein binding sites in protein structures using hidden Markov support vector machine',
#         'Clinical entity recognition using structural support vector machines with rich features'])