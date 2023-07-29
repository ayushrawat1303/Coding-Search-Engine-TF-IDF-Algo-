# Import required libraries
from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By as by

# CSS selectors for the page elements to extract data from
body_class = ".px-5.pt-4"
heading_class = ".mr-2.text-label-1"

# Function to write data to separate files for each component
def writeToFile2(heading, body, index, pageUrl):
    # Create directories if they do not exist
    os.makedirs('questionContent', exist_ok=True)
    os.makedirs('questionLinks', exist_ok=True)
    os.makedirs('questionHeadings', exist_ok=True)
    # Write page content to questionContent/questionContentLeetcode{index}.txt
    file = open(f'questionContent/questionContentLeetcode{index}.txt', 'w', encoding="utf-8")
    file.write(str(index) + "\t" + heading + "\n" + body)
    file.close()

    # Write page URL to questionLinks/questionsLink_{index}.txt
    file = open(f'questionLinks/questionsLink_{index}.txt', 'w', encoding="utf-8")
    file.write(pageUrl)
    file.close()

    # Write page heading to questionHeadings/questionsName_{index}.txt
    file = open(f'questionHeadings/questionsName_{index}.txt', 'w', encoding="utf-8")
    file.write(heading)
    file.close()

# Function to open the browser and return the driver instance
def openBrowser(url):
    service = Service(ChromeDriverManager().install())
    # Open the Chrome browser in headless mode (without a visible window)
    Options = webdriver.ChromeOptions()
    Options.add_argument("--ignore-certificate-errors")
    Options.add_experimental_option("excludeSwitches", ["enable-logging"])
    Options.add_argument("--incognito")
    Options.add_argument("--headless")

    # Create a new instance of the Chrome web driver
    driver = webdriver.Chrome(service=service, options=Options)

    # Load the web page with the provided URL
    driver.get(url)
    driver.maximize_window()
    return driver

# Function to close the browser
def closeBrowser(browser):
    # Quit the browser and close all associated windows
    browser.quit()

# Function to extract data from a single page and save it to files
def singlePageData(pageUrl, index):
    try:
        # Open the browser and load the web page
        browser = openBrowser(pageUrl)

        # Wait for the specified elements to appear on the page
        time.sleep(2)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((by.CSS_SELECTOR, body_class)))
        time.sleep(1)

        # Extract the heading and body content from the page
        headingContent = browser.find_element(by.CSS_SELECTOR, heading_class)
        bodyContent = browser.find_element(by.CSS_SELECTOR, body_class)

        # If the body content is not empty, write the data to files
        if bodyContent.text:
            writeToFile2(headingContent.text, bodyContent.text, index, pageUrl)
            print("    ----------->  saving data ")

        time.sleep(1)
        return True

    except Exception as e:
        # If any error occurs during the process, print the error message and the page URL
        print(f"    ----------->  Error in {e} \n {pageUrl} ")
        return False

# Function to get links from a file and return them as an array
def getArrLinks():
    # Read the links from the file and store them in an array
    file = open('parser\questionsLink.txt', 'r')
    arr = []
    for line in file:
        arr.append(line.strip())  # Remove any leading/trailing whitespace characters
    file.close()
    return arr

# Main function to process the links and extract data from each page
def main_function():
    index = 1
    arr = getArrLinks()

    # Getting data from single page
    for link in arr:
        success = singlePageData(link, index)
        if success:
            index = index + 1

if __name__ == "__main__":
    main_function()
