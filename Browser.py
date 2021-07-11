from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


class ChromeBrowser:
    def __init__(self):
        self.__proxy_file = open('proxies.txt')
        self.__options = Options()
        self.__ua = UserAgent()
        self.__chrome_agent = self.__ua.random
        self.__options.add_argument('log-level=3')
        self.__options.add_argument('window-size=1920x1080')
        self.__options.add_argument(f'user-agent={self.__chrome_agent}')
        # self.__options.add_argument('--proxy-server=%s' % '58.8.85.128:8080')
        self.__driver = webdriver.Chrome(options=self.__options)

    def getDriver(self):
        if self.__driver is not None:
            return self.__driver
