import base64
import sys
import os
import inspect
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import *
import atexit
from config import *

def isLinux():
    return sys.platform == 'linux'


def isWindows():
    return sys.platform == 'win32'


# Scrapper Class using selenium
class Scrapper(object):
    def __init__(self):
        # Automation contructor
        print("Start scrapping")

    # initialize Firefox
    def InitializeFirefox(self):        
        if isLinux():
            fp = webdriver.FirefoxProfile()            
        elif isWindows():
            fp = webdriver.FirefoxProfile()            
        else:
            fp = webdriver.FirefoxProfile()
            
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.accept_untrusted_certs = True
        fp.set_preference("browser.download.dir", self.download_path)
        fp.set_preference("dom.webnotifications.enabled", False)
        fp.set_preference('browser.helperApps.neverAsk.saveToDisk','application/x-file-to-save,text/csv,application/octet-stream,application/*,text/*,application/xls,application/csv,text/plain,application/vnd.ms-excel,text/comma-separated-values,application/excel')
        fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        fp.set_preference("browser.download.dir", self.download_path)
        fp.set_preference("javascript.enabled", False)
        fp.update_preferences()

        if isLinux():
            self.driver = webdriver.Firefox(firefox_profile=fp)
            self.wait = WebDriverWait(self.driver, 60, poll_frequency=1,ignored_exceptions=[NoSuchElementException, ElementNotVisibleException,ElementNotSelectableException])
            self.driver.implicitly_wait(60)
        
        else:
            self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',desired_capabilities=DesiredCapabilities.FIREFOX, browser_profile=fp)
            self.wait = WebDriverWait(self.driver, 150, poll_frequency=1,ignored_exceptions=[NoSuchElementException, ElementNotVisibleException,ElementNotSelectableException])
            self.driver.implicitly_wait(150)
            
        self.driver.maximize_window()
        self.current_handle = self.driver.current_window_handle

    #  Initialize Chrome
    def InitializeChrome(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4280.141 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))

        #self.driver = webdriver.Chrome(chrome_options=options)
        self.driver = webdriver.Chrome('.\\chromedriver.exe')
        self.wait = WebDriverWait(self.driver, 150, poll_frequency=1,ignored_exceptions=[NoSuchElementException, ElementNotVisibleException,ElementNotSelectableException])
        self.driver.implicitly_wait(150)
        
        self.driver.maximize_window()
        self.current_handle = self.driver.current_window_handle

    def GoToURL(self, url, wait=15):
        self.driver.set_page_load_timeout(wait)

        while True:
            try:
                self.driver.get(url)
                break
            except TimeoutException:
                print("*** Retrying: " + url)

        self.driver.set_page_load_timeout(120)    

    def GetEleByXpath(self, xpath, no_wait=False, return_on_retry=False):
        if no_wait:
            self.ele = self.driver.find_element_by_xpath(xpath)
        else:            
            self.ele = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return self.ele

    def ClickXpath(self, xpath=None, no_wait=False):
        if xpath is not None:
            ele = self.GetEleByXpath(xpath, no_wait)
        else:
            ele = self.ele
        ele.click()

    def SendKeysXpath(self, text, xpath=None, no_wait=False):
        if xpath is not None:
            ele = self.GetEleByXpath(xpath, no_wait)
        else:
            ele = self.ele
    
        ele.send_keys(text)

    def CheckExistsByXpath(self, xpath, wait=3, ele=None):
        self.driver.implicitly_wait(wait)
        try:
            if ele is None:
                self.ele = self.driver.find_element_by_xpath(xpath)
            else:
                self.ele = ele.find_element_by_xpath(xpath)
        except NoSuchElementException:
            self.driver.implicitly_wait(60)
            return False
        try:
            if self.ele.is_displayed():
                self.driver.implicitly_wait(60)
                return True
            else:
                self.driver.implicitly_wait(60)
                return False
        except:
            self.driver.implicitly_wait(60)
            return False

    def GetTextOfEleByXpath(self, xpath=None, no_wait=False):
        if xpath is not None:
            ele = self.GetEleByXpath(xpath, no_wait)
        else:
            ele = self.ele
        text = ele.text
        return text

    def Login(self):
        user = stock_user
        passwd = stock_pass
        
        try:
            start_url = "https://jonahlupton.substack.com/"
            
            self.GoToURL(start_url)
            
           

            if self.CheckExistsByXpath("//a[@class='login-button']", wait=0):
                self.ClickXpath()


            # if self.CheckExistsByXpath("//a[@class='login-option']", wait=0):
            if self.CheckExistsByXpath("//a[contains(text(), 'log in with')]", wait=0):
                self.ClickXpath()
            
            # if self.CheckExistsByXpath("//kat-button[@id='sign-in-button']", wait=0):
            #     self.ClickXpath()
            
            while True:
                    
                if self.CheckExistsByXpath("//span[@class='account-info-logout']", wait=0):
                    return {'status': True}

            # self.SendKeysXpath(user, "//input[@name='email']")
            # self.SendKeysXpath(passwd, "//input[@name='password']")
            # self.ClickXpath("//button[@type='submit']")

            # if self.CheckExistsByXpath('//div[contains(text(), "User not found")]'):
            #     return {'status': False, 'message': 'User not found'}
            
            # if self.CheckExistsByXpath('//div[contains(text(), "Password incorrect")]'):
            #     return {'status': False, 'message': 'Incorrect password'}
            
            # return {'status': True}
        except Exception as error:
            return {'status': False, 'message': 'Something went wrong'}


    def NavigateToFirstPost(self):
        #Scrapper.driver.execute_script('$("#sc-navtab-reports").toggleClass("nav-open")')
        if self.CheckExistsByXpath("/html/body/div[1]/div/div[2]/div[2]/div[2]/a[1]", wait=3):
            title = self.GetTextOfEleByXpath()
            print(title)
          
            if "Interview" in title :
                return False
            if "Webcast" in title :
                return False
            if "Webinar" in title :
                return False
            if "Chat" in title :
                return False
            
            print("----------------------In Post------------------------")
            self.ClickXpath()
            return True

    def GetPostContent(self):
        if self.CheckExistsByXpath("//*[@id='main']/div[2]/div/div[1]/div/article", wait=3):
            return self.GetTextOfEleByXpath()

        return "Not found!"
    