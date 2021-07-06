from TempMail import TempMail
from Browser import ChromeBrowser
import time
from gibberish import Gibberish
import censusname
from password_generator import PasswordGenerator
import random
from selenium.webdriver.support.ui import Select


class Instagram:
    def __init__(self):
        self.__pwo = PasswordGenerator()
        self.__username = None
        self.__password = self.__pwo.non_duplicate_password(10)
        self.__driver = ChromeBrowser().getDriver()
        self.__gib = Gibberish()
        self.__name = censusname.generate()
        self.__my_mail = TempMail()
        self.__my_mail.new_email()
        self.__driver.get('https://www.instagram.com/accounts/emailsignup/')

    def create_account(self):
        if self.__driver.current_url == 'https://www.instagram.com/accounts/emailsignup/':
            time.sleep(3)
            self.__driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[3]/div/label/input').send_keys(
                self.__my_mail.get_email_address())
            self.__driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[4]/div/label/input').send_keys(
                self.__name)
            self.__username = '_'.join(self.__gib.generate_word(4))
            while len(self.__username) > 30:
                self.__username = '_'.join(self.__gib.generate_word(4))
            self.__driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[5]/div/label/input').send_keys(
                self.__username)
            self.__driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[6]/div/label/input').send_keys(
                self.__password)
            self.__driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div[1]/div/form/div[7]/div/button').click()
            rand_year = random.randint(1970, 2005)
            rand_day = random.randint(1, 28)
            rand_month = random.randint(1, 12)
            self.__driver.implicitly_wait(2)
            month_selector = Select(self.__driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select'))
            month_selector.select_by_value(str(rand_month))
            self.__driver.implicitly_wait(2)
            day_selector = Select(self.__driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select'))
            day_selector.select_by_value(str(rand_day))
            self.__driver.implicitly_wait(2)
            year_selector = Select(self.__driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select'))
            year_selector.select_by_value(str(rand_year))
            self.__driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div/div[1]/div/div[6]/button').click()
            check_mail = self.__my_mail.check_emails()
            while not check_mail:
                check_mail = self.__my_mail.check_emails()
            self.__my_mail.read_emails()
            the_content = self.__my_mail.get_content()
            print(the_content)
        else:
            self.__driver.get('https://www.instagram.com/accounts/emailsignup/')
            time.sleep(1)
            self.create_account()

    def get_account_info(self):
        info = [[self.__username, self.__password, self.__name, self.__my_mail.get_email_address()]]
        return info

    def __del__(self):
        self.__driver.close()
