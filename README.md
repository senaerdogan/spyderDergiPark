A python library for searching and downloading articles from DergiPark which is a website where people can browse articles based on numerous filters . 

1. First, install a driver from the driver links listed here: https://pypi.org/project/selenium/

2. To download articles, you should run **searchAndDownload** method. There are a few parameters to consider: 
   1. topic: (default None) This is the topic you want to search for. It is limited with the topics listed in DergiPark. To access these topics and their corresponding links, check out 'topicLinkDict.pickle' file. It may be in a different path if specified. 
   2. searchPhrase: (default None) This is the phrase you want to search for. There is no limitation.
   3. maxArticle: (default None) DergiPark lists at most 9600 articles. If maxArticle is not specified, the code will download at most 9600 articles. You can change this parameter if you want to download less than 9600 articles. You must not give a number greater than 9600. 
   4. headless: (default True) If you want to see the browser while downloading, set it to False. 
   5. language: (default türkçe) Specify the article language. If the authors didn't specify the article language, this article won't be downloaded. You should give one language at a time. 
   6. path: (default None) Specify the where to download the articles. If not specified, creates an articles folder. 
   7. progress: (default True) Whether to see a progress bar while downloading. Set it to False if you don't want to see it. 
   8. console_logging: (default False) Whether you want to see an output in the console for each article downloaded. 
   9. driver_path: (default None) Specify the driver path. 
   
3. If you want to renew the topic dictionary, please call  refreshTopicPickle method with these parameters:
   1. dictPath: (default topicLinkDict.pickle) Specify the pickle you want to write the dictionary.
   2. driverPath: (default None) Specify the driver path.

All tests were conducted using chromedriver. 