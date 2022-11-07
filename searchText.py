from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# import TimeUnit
from selenium.webdriver.support.ui import WebDriverWait

import json
options = webdriver.ChromeOptions()
# Path to your chrome profile
options.add_argument("user-data-dir=/home/hieu/.config/google-chrome/default")
# options.add_argument('--user-data-dir=C:/Users/GOD/AppData/Local/Google/Chrome/User Data')

options.add_argument('--profile-directory=Profile 3')

driver = webdriver.Chrome(service=ChromeService(
    executable_path=ChromeDriverManager().install()), chrome_options=options)


def loadCookies():
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
        for cookie in cookies:
            # check same site
            # if cookie['sameSite'] == 'None':
            driver.add_cookie(cookie)


# loadCookies()
driver.get("https://chat.zalo.me/")
actions = ActionChains(driver)
# find element data-id = div_Main_TabCT


def inputSearch(query):
    textbox = WebDriverWait(driver, 40).until(EC.presence_of_element_located(
        (By.XPATH, "//input[@id='contact-search-input']")))
    # input search query
    textbox.send_keys(query)
    time.sleep(1)
    driver.find_element(
        By.XPATH, "//div-b14[@data-translate-inner=\"STR_TAB_MESSAGE\"]").click()


def getMessage():
    # find message container
    messageContainer = driver.find_element(
        By.XPATH, "//*[contains(@style,'position: absolute; inset: 0px; overflow: scroll; margin-right: -7px; margin-bottom: -7px;')]")
    actions.move_to_element(messageContainer).perform()
    while True:
        messages = driver.find_elements(
            By.XPATH, "//*[starts-with(@id,'search-item')]")
        for message in messages:
            message.click()
            # find message content
            # time.sleep(2)
            messageContent = WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class,'highlighted')]")))
            #  = driver.find_element()
            #log to file
            print(messageContent.text)
            output = open("output.txt", "a")
            output.write(messageContent.text)
            output.write("\n")
            output.close()
        actions.move_to_element(messages[-1]).perform()
        newMessages = driver.find_elements(
            By.XPATH, "//*[starts-with(@id,'search-item')]")
        if newMessages[-1]  == messages[-1]:
            break
        else:
            messages = newMessages

inputSearch("hi")
input()
getMessage()
