from selenium import webdriver


class Settings:
    def __init__(self, path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"):
        self.path = path
        chrome_options = webdriver.ChromeOptions()
        pref = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", pref)
        browser = webdriver.Chrome(self.path, chrome_options=chrome_options)
        browser.implicitly_wait(10)
        self.browser = browser

