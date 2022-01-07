import pickle
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

with open('topicLinkDict.pickle', 'rb') as handle:
    topicLinkDict = pickle.load(handle)


options = Options()
options.headless = True
s = Service("chromedriver.exe")
#for headless start: webdriver.Chrome( options= options, service=s)
driver = webdriver.Chrome(  service=s)

driver.get(topicLinkDict['hukuk'])
time.sleep(5)

numberOfPages = int(driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[2]/div[3]/ul/li[8]/a').get_attribute("textContent"))
currentPage = 1
numberOfArticlesPerPage = len(driver.find_elements(By.XPATH, '//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div'))

while (currentPage <= numberOfPages):
    article = 1
    while (article <= numberOfArticlesPerPage):
        driver.find_element(By.XPATH,'//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div[{article:d}]/div/h5/a'.format(article=article)).click()
        time.sleep(2)
        language = "".join(driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td").get_attribute("textContent").lower().split())
        if (language == "türkçe"):
            pdfLink = driver.find_element(By.XPATH, '//*[@id="article-toolbar"]/a[1]').get_attribute("href")
            print(pdfLink)
            response = requests.get(pdfLink)
            #save with doi number
            pdf = open("./articles/{article:d}.pdf".format(article= currentPage*article), 'wb')
            pdf.write(response.content)
            pdf.close()
            print("File downloaded")
            time.sleep(5)
            driver.execute_script("window.history.go(-1)")
            time.sleep(1)
        article += 1
    currentPage += 1
    driver.get("https://dergipark.org.tr/tr/search/{PAGE:d}?section=articles&aggs%5Bsubjects.id%5D%5B0%5D=321".format(PAGE= currentPage))

    if currentPage == 4:
        break

driver.quit()
