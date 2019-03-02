from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
def sele_ei(name, titles):
    for title in titles:
        browser.get('https://www.engineeringvillage.com/search/quick.url')
        input = browser.find_element_by_id('search-word-1')
        input.send_keys(title)
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='abstractlink']")))

        name_list = sorted(name.replace(',', '').lower().split(' '))
        print(name_list)

        article_list = browser.find_elements_by_xpath("//div[@class='row result-row']")
        for i in range(len(article_list)):
            author_list = [sorted(x.get_attribute('text').replace(',', '').lower().split(' ')) for x in browser.find_elements_by_xpath("//div[@id='result_{}']/div/div/div/div/div/a[@class='authorSearchLink']".format(str(i)))]
            #通过比对姓名进行判断是否为寻找的论文
            if name_list in author_list:
                link = browser.find_element_by_xpath("//div[@id='result_{}']/div/div/div/div/div/h3/a[@class='abstractlink']".format(str(i))).get_attribute('href')
                print('link:' + link)
                browser.get(link)
                wait.until(EC.presence_of_element_located((By.ID, 'abstractWrappper')))
                break
        details = {}

#传入姓名与论文title的列表进行ei上的爬取
sele_ei('Buzhou Tang', ['Recognizing clinical entities in hospital discharge summaries using Structural Support Vector Machines with word representation features',
         'Prediction of protein binding sites in protein structures using hidden Markov support vector machine'])