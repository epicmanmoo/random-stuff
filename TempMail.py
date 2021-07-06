from Browser import ChromeBrowser
import time
from datetime import date
import pyperclip
from selenium.common.exceptions import NoSuchElementException


class TempMail:
    def __init__(self):
        self.__driver = ChromeBrowser().getDriver()
        self.__email_address = None
        self.__created_date = None
        self.__inbox_size = 0
        self.__emails_xpath = []
        self.__content = []

    def new_email(self):
        if self.__driver.current_url == 'https://temp-mail.org/en/':
            self.__driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(5)
            self.__driver.find_element_by_xpath('//*[@id="click-to-copy"]').click()
            self.__email_address = pyperclip.paste()
            self.__created_date = date.today()
        else:
            self.__driver.get('https://temp-mail.org/en/')
            time.sleep(1)
            self.new_email()

    def check_emails(self):
        self.__driver.refresh()
        if self.__driver.current_url == 'https://temp-mail.org/en/':
            self.__driver.execute_script("window.scrollTo(0, 500)")
            index_pos = 2
            flag = False
            while True:
                try:
                    self.__driver.implicitly_wait(5)
                    cur_email_xpath = f'//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/ul/li[{index_pos}]'
                    if self.__driver.find_element_by_xpath(cur_email_xpath).is_displayed():
                        self.__emails_xpath.append(cur_email_xpath)
                        index_pos += 1
                except NoSuchElementException:
                    flag = True
                    break
            if flag and index_pos == 2:
                return False
            self.__inbox_size = index_pos - 1
            return True
        else:
            self.__driver.get('https://temp-mail.org/en/')
            time.sleep(1)
            self.check_emails()

    def read_emails(self):
        if self.__driver.current_url == 'https://temp-mail.org/en/':
            for email_xpath in self.__emails_xpath:
                self.__driver.execute_script("window.scrollTo(0, 500)")
                self.__driver.find_element_by_xpath(email_xpath).click()
                time.sleep(3)
                cur_email_subject = self.__driver.find_element_by_xpath(
                    '//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/h4').text
                # cur_email_body = self.__driver.find_element_by_xpath(
                #     '//*[@id="tm-body"]/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[3]')
                cur_email_body = 'n/a'
                self.__content.append([cur_email_subject, cur_email_body])
                self.__driver.get('https://temp-mail.org/en/')
                time.sleep(3)
        else:
            self.__driver.get('https://temp-mail.org/en/')
            time.sleep(1)
            self.read_emails()

    def get_content(self):
        return self.__content

    def get_email_address(self):
        if self.__email_address is not None:
            return self.__email_address

    def get_created_date(self):
        if self.__created_date is not None:
            return self.__created_date

    # def __del__(self):
    #     self.__driver.close()
