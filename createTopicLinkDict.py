from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import pickle
import re

def createTopicLinkDict(dictPath = "topicLinkDict.pickle"):
    options = Options()
    options.headless = True
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome( options=options, service=s)

    driver.get("https://dergipark.org.tr/tr/search?section=articles")
    time.sleep(5)

    lastException = 0
    i = 2
    topicLinkDict = {}

    while True:
        try:
            topic = re.sub(r'[^\w\s]', '', "".join(driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[{order:d}]/div[1]/a/div".format(order=i)).get_attribute("textContent").lower().split()))
            link = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[{order:d}]/a".format(order=i)).get_attribute("href")
            print(i)
            print(topic)
            topicLinkDict[topic] = link
            i += 1
        except NoSuchElementException:
            if (i-lastException) == 1:
                with open(dictPath, 'wb') as handle:
                    pickle.dump(topicLinkDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("done")
                break
            lastException = i
            i += 1
            continue

    driver.quit()