from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By as by
from webdriver_manager.chrome import ChromeDriverManager
import re

siteUrl = "https://leetcode.com/problems/"
pageTitle = "Problems - LeetCode"


def writeToFile(questionLinkList):
    file = open('questionsLink.txt','w')
    for x in questionLinkList:
        file.write(x+"\n")
    file.close()

def openBrowser(url):
    service = Service(ChromeDriverManager().install())
    print("    ----------->  Opening Browser")
    Options = webdriver.ChromeOptions()
    Options.add_argument("--ignore-certificate-errors")
    Options.add_experimental_option("excludeSwitches", ["enable-logging"])
    Options.add_argument("--incognito")
    Options.add_argument("--headless")
    
    # initiating chromedriver
    driver = webdriver.Chrome(service=service, options=Options)
    
    driver.get(url)
    driver.maximize_window()
    return driver

def closeBrowser(browser):
    print("    ----------->  Closing Browser")
    browser.quit()
    
def check(string, sub_str):
    match = re.search(sub_str, string)
    if match:
        return True
    else:
        return False
    
def fetchPageData(pageUrl):
    browser = openBrowser(pageUrl)
    time.sleep(3)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.title_contains(pageTitle))
    
    if (browser.title == pageTitle):
        print("    ----------->  parsing data ")
        
        links = browser.find_elements(by.TAG_NAME, "a")
        # Iterate over each 'a' element
        questionLinkList = []
        
        for i in links:
            try:
                # only take those links which have /problems in their href
                if "/problems/" in i.get_attribute("href"):
                    # and we only want problems and not solution links
                    pattern = "/solution"
                    x = check(i.get_attribute("href"),pattern)
                    if x == False:
                        questionLinkList.append(i.get_attribute("href"))
            except:
                pass
        # Remove duplicate links using set
        questionLinkList = list(set(questionLinkList))   
            
        print("    ----------->  saving data ")
        time.sleep(1)
        print("    ----------->  done ")
        closeBrowser(browser)
        return questionLinkList
    else :
        print("    ----------->  connection failed ")
        return -1
   
def getData():
    try:
        browser = openBrowser(siteUrl)
        time.sleep(2)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.title_contains(pageTitle))
        
        if (browser.title == pageTitle):
            closeBrowser(browser)
            
            questionLinkList = []
            
            #Fetching data from each page
            for page in range(1,56):
                print(
                    f"    ----------->  Fetching data from page : {page} of 55 \n\n"
                )
                pageUrl = siteUrl + '?page=' + str(page)
                questionLinkList += fetchPageData(pageUrl) 
            
            print("    ----------->  done all pages")
            print(f" total {questionLinkList.__len__()} question fetched")  
            writeToFile(questionLinkList)
        
        else :
            print("    ----------->  connection failed ")
            return
            
    except Exception as e:
        print("    ----------->  Error in getData() : ", e)
        return    
    

if __name__ == "__main__":
    getData()