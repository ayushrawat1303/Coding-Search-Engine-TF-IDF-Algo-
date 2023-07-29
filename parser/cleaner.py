import re
import os

# Common words to be removed from the processed text
common_words = ["Input", "Output", "Explaination", "Example", "the", "a", "an", "is", "are", "and", "in", "of", "to", "that", "or", "at"]

# Function to write processed page content to a file
def writeToFile(pageContent, index):
    os.makedirs('cleanedQuestion', exist_ok=True)
    file = open(f'cleanedQuestion/questionContentLeetcode{index}.txt', 'w')
    file.write(pageContent)
    file.close()

# Function to read page content from a file
def getPageContent(index):
    target_directory = f'questionContent\questionContentLeetcode{index}.txt'
    file = open(target_directory, 'r', encoding='utf-8')
    content = file.read()
    file.close()
    return content

# Function to remove unwanted patterns and common words from the page content
def remove(pattern, pageContent):
    pageContent = re.sub(r'\d+', '', pageContent)
    pageContent = re.sub(pattern, '', pageContent)
    pageContent = re.sub(r'\s+', ' ', pageContent).strip()
    pageContent = re.sub(r'[^\w\s]', '', pageContent)
    pageContent = re.sub(r'\b\w\b', '', pageContent)
    pageContent = ' '.join([word for word in pageContent.split() if word.lower() not in common_words])
    return pageContent

# Main function to process page contents for multiple links
def main_function():
    num_of_links = 2020  # Define the total number of links/pages to process
    
    for index in range(1, num_of_links + 1):
        # reading all the questions content from questionscontent file
        pageContent = getPageContent(index)

        # removing all the unneccessary data from it
        pattern = r'\[.*?\]'
        
        pageContent = remove(pattern, pageContent)
        
        # write the cleaned pagecontent into new file
        writeToFile(pageContent, index)

if __name__ == "__main__":
    main_function()