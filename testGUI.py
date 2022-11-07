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
options.add_argument("user-data-dir=/home/hieu/.config/google-chrome/default") #Path to your chrome profile
# options.add_argument('--user-data-dir=C:/Users/GOD/AppData/Local/Google/Chrome/User Data')

options.add_argument('--profile-directory=Profile 3')

driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()), chrome_options=options)

def loadCookies():
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
        for cookie in cookies:
            #check same site
            # if cookie['sameSite'] == 'None':            
            driver.add_cookie(cookie)
# loadCookies()            
driver.get("https://chat.zalo.me/")
actions = ActionChains(driver)
#find element data-id = div_Main_TabCT

from selenium.webdriver.support import expected_conditions as EC

try:
    # input()
    element = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "//*[@data-id='div_Main_TabCT']")))
    print("found")

    element = driver.find_element(By.XPATH, "//*[@data-id='div_Main_TabCT']")
    #wait for element to be clickable
    actions.move_to_element(element).perform()
    #click on element
    element.click()

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id,'friend-item')]")))
    #get friend container with class = "ReactVirtualized__Grid__innerScrollContainer"
    friendContainer = driver.find_element(By.XPATH, "//*[contains(@style,'position: absolute; inset: 0px; overflow: scroll; margin-right: -7px; margin-bottom: -7px;')]")    
    print(friendContainer.accessible_name)

    #move cursor to friend container
    actions.move_to_element(friendContainer).perform()
    
    friends = driver.find_elements(By.XPATH, "//*[starts-with(@id,'friend-item')]")
    friendsList = set(friends)
    lastFriend = friends[-1]
    nameDict = {}
    while True:
        #scroll to last friend
        actions.move_to_element(lastFriend).perform()
        # wait 1s
        # driver.manage().timeouts().implicitlyWait(1000)
        time.sleep(0.1)
        # element = WebDriverWait(driver, ).until(EC.element_to_be_clickable((By.XPATH, "//*[starts-with(@id,'friend-item')]")))
        #get all friends
        friends = driver.find_elements(By.XPATH, "//*[starts-with(@id,'friend-item')]")
        if lastFriend == friends[-1]:
            break
        lastFriend = friends[-1]
        friendsList = friendsList.union(set(friends))
        print(len(friends))

    print(len(friendsList))
    for friend in friendsList:
        #find span with class = "friend-name"
        name = friend.find_element(By.XPATH, "//*[contains(@class,'truncate')]")
        print(name.text)
    input()
finally:
    driver.quit()
