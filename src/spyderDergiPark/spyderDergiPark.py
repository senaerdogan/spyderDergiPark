import pickle
import time
import requests
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from pathlib import Path
from .createTopicLinkDict import createTopicLinkDict
from tqdm import tqdm


def defineDriverPath(path):
    if path is None:
        return "chromedriver.exe"
    return path


def defineOutputPath(path):
    if path is None:
        return "articles"
    return path


def loadDriver(headless, driverPath):
    options = Options()
    options.headless = True
    s = Service(driverPath)

    if headless:
        driver = webdriver.Chrome(options=options, service=s)
    else:
        driver = webdriver.Chrome(service=s)
    return driver


def refreshTopicPickle(dictPath="topicLinkDict.pickle", driverPath=None):
    driverPath = defineDriverPath(driverPath)
    createTopicLinkDict(dictPath, driverPath)


def loadTopicPickle(dictPath="topicLinkDict.pickle", driverPath=None):
    try:
        with open(dictPath, 'rb') as handle:
            topicLinkDict = pickle.load(handle)
        return topicLinkDict
    except FileNotFoundError:
        driverPath = defineDriverPath(driverPath)
        refreshTopicPickle(dictPath, driverPath)
        with open(dictPath, 'rb') as handle:
            topicLinkDict = pickle.load(handle)
        return topicLinkDict


def getNumberOfArticlesToDownload(driver, maxArticle):
    if maxArticle is None:
        # total articles
        return 9600 #DergiPark currently lists max 9600 articles. May need to change it later.
        #return int("".join(driver.find_element(By.XPATH, '//*[@id="search-sections"]/div[1]/a/span[2]/span[2]').get_attribute("textContent").split(".")))
    return maxArticle


def download(driver, maxArticle, language, current_url, path, progress, console_logging):
    path = defineOutputPath(path)
    Path(path).mkdir(parents=True, exist_ok=True)
    numberOfPages = int(driver.find_element(By.XPATH,
                                            '/html/body/div[2]/div/div/div/div/div/div/div[2]/div[2]/div[2]/div[3]/ul/li[8]/a').get_attribute(
        "textContent"))
    currentPage = 1
    numberOfArticlesPerPage = len(
        driver.find_elements(By.XPATH, '//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div'))

    numberOfArticlesToDownload = getNumberOfArticlesToDownload(driver, maxArticle)
    if progress:
        pbar = tqdm(total=numberOfArticlesToDownload)
    numberOfDownloaded = 0

    while currentPage <= numberOfPages:
        article = 1
        while article <= numberOfArticlesPerPage:
            number_of_try = 0
            try:
                driver.find_element(By.XPATH,
                                    '//*[@id="kt_content"]/div[2]/div[2]/div[2]/div[2]/div[{article:d}]/div/h5/a'.format(
                                        article=article)).click()
                time.sleep(2)
                languageArticle = "".join(driver.find_element(By.XPATH,
                                                              '//*[@id="kt_content"]/div/div[2]/div[1]/div[2]/div/table/tbody/tr[1]/td').get_attribute(
                    "textContent").lower().split())
                if languageArticle == language:
                    pdfLink = driver.find_element(By.XPATH, '//*[@id="article-toolbar"]/a[1]').get_attribute("href")
                    if console_logging:
                        print(pdfLink)
                    response = requests.get(pdfLink)
                    try:
                        # doi number
                        doiLink = driver.find_element(By.XPATH, '//*[@id="article_en"]/div[1]/a').get_attribute(
                            "textContent").split("/")
                        articleFileName = "-".join(doiLink[-2:])
                    except NoSuchElementException:
                        articleFileName = str(currentPage) + "-" + str(article)
                    pdf = open("./{path:s}/{article:s}.pdf".format(path=path, article=articleFileName), 'wb')
                    pdf.write(response.content)
                    pdf.close()
                    if console_logging:
                        print("File downloaded")
                    time.sleep(3)
                    numberOfDownloaded += 1
                    if progress:
                        pbar.update(1)

                driver.execute_script("window.history.go(-1)")
                time.sleep(1)
                article += 1
                if numberOfDownloaded == numberOfArticlesToDownload:
                    break
            except Exception:
                if number_of_try == 3:
                    continue
                number_of_try += 1
                time.sleep(1)

        if numberOfDownloaded == numberOfArticlesToDownload:
            break
        currentPage += 1
        new_page = current_url.replace("search", "search/{PAGE:d}".format(PAGE=currentPage))

        driver.get(new_page)
    pbar.close()


def searchByTopic(topic, maxArticle=None, headless=False, language="türkçe", driverPath=None):
    language = "".join(language.lower().split())
    topic = "".join(topic.lower().split())
    driverPath = defineDriverPath(driverPath)
    driver = loadDriver(headless, driverPath)
    topicLinkDict = loadTopicPickle(driverPath=driverPath)
    driver.get(topicLinkDict[topic])
    time.sleep(5)

    current_url = driver.current_url
    return driver, current_url


def searchByPhrase(searchPhrase, maxArticle=None, headless=False, language="türkçe", driverPath=None):
    language = "".join(language.lower().split())
    driver = loadDriver(headless, defineDriverPath(driverPath))
    driver.get('https://dergipark.org.tr/tr/search?q=&section=articles')
    time.sleep(5)

    searchBar = driver.find_element(By.XPATH, '//*[@id="search-form"]/div/input')
    searchBar.send_keys(searchPhrase)
    time.sleep(2)

    searchBar.send_keys(Keys.ENTER)
    time.sleep(1)
    current_url = driver.current_url
    return driver, current_url


def searchByTopicAndPhrase(topic, searchPhrase, maxArticle=None, headless=False, language="türkçe", driverPath=None):
    language = "".join(language.lower().split())
    topic = "".join(topic.lower().split())
    driverPath = defineDriverPath(driverPath)
    driver = loadDriver(headless, driverPath)
    topicLinkDict = loadTopicPickle(driverPath=driverPath)
    driver.get(topicLinkDict[topic])
    time.sleep(5)

    searchBar = driver.find_element(By.XPATH, '//*[@id="search-form"]/div/input')
    searchBar.send_keys(searchPhrase)
    time.sleep(2)

    searchBar.send_keys(Keys.ENTER)
    time.sleep(1)
    current_url = driver.current_url
    driver.get(current_url)
    return driver, current_url


def searchAndDownload(topic=None, searchPhrase=None, maxArticle=None, headless=True, language="türkçe", path=None,
                      progress=True, console_logging=False, driver_path=None):
    if (topic is None) and (searchPhrase is None):
        raise Exception("At least one of the topic or search phrase must be specified!")
    elif (topic is not None) and (searchPhrase is not None):
        driver, current_url = searchByTopicAndPhrase(topic, searchPhrase, maxArticle, headless, language, driver_path)
        download(driver, maxArticle, language, current_url, path, progress, console_logging)
    elif topic is not None:
        driver, current_url = searchByTopic(topic, maxArticle, headless, language, driver_path)
        download(driver, maxArticle, language, current_url, path, progress, console_logging)
    elif searchPhrase is not None:
        driver, current_url = searchByPhrase(searchPhrase, maxArticle, headless, language, driver_path)
        download(driver, maxArticle, language, current_url, path, progress, console_logging)

