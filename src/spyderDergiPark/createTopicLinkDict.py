from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import pickle
import re
from tqdm import tqdm

def createTopicLinkDict(dictPath, driverPath):
    options = Options()
    options.headless = True
    s = Service(driverPath)
    driver = webdriver.Chrome(options=options, service=s)

    print('Dictionary creation begins.')
    driver.get("https://dergipark.org.tr/tr/search?section=articles")
    time.sleep(5)

    lastException = 0
    i = 2
    topicLinkDict = {}

    numberOfTopics = len(
        driver.find_elements(By.XPATH, '//*[@id="collapsible_portlet_2"]/div[2]/div/div'))

    numberOfGroups = len(driver.find_elements(By.XPATH,'//*[@id="collapsible_portlet_2"]/div[2]/div/div[contains(@class, "kt-widget-18__item bucket-group-title ")]'))

    pbar = tqdm(total=numberOfTopics-numberOfGroups)

    while True:
        try:
            topic = re.sub(r'[^\w\s]', '', "".join(driver.find_element(By.XPATH,
                                                                       "/html/body/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[{order:d}]/div[1]/a/div".format(
                                                                           order=i)).get_attribute(
                "textContent").lower().split()))
            link = driver.find_element(By.XPATH,
                                       "/html/body/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[{order:d}]/a".format(
                                           order=i)).get_attribute("href")

            topicLinkDict[topic] = link
            i += 1
        except NoSuchElementException:
            if (i - lastException) == 1:
                with open(dictPath, 'wb') as handle:
                    pickle.dump(topicLinkDict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    pbar.update(1)
                break
            lastException = i
            i += 1
            continue
        pbar.update(1)

    print('Dictionary created.')
    pbar.close()
    driver.quit()

