import os
import re
import string
import math
import json

def preprocess_name(name):
    # Remove numbers from the name
    pattern = r'\d+'
    name = re.sub(pattern, ' ', name)
    
    # Remove dots and starting/ending spaces
    name = name.replace('.', ' ')
    name = name.strip()
    
    return name

def writeToVacab(vocab):
    # Write vocab to a file named "document.txt"
    with open("document.txt", "w", encoding="utf-8") as f:
        f.write(vocab)
        f.close()
        
    # Store all the words from vocab string to a set
    vocab = vocab.split()
    vocab = set(vocab)
    return vocab
    f.close()
        
def cleaningData(data):
    # Lowercase the data
    data = data.lower()
    
    # Remove the "Example" section from the data
    data = data.split("Example 1")[0]
    
    # Remove digits from the data
    pattern = r'\d+'
    data = re.sub(pattern, ' ', data)
    
    # Remove punctuations
    translator = str.maketrans('', '', string.punctuation)
    data = data.translate(translator)
    
    # Remove extra spaces and next lines
    data = data.replace('\n', ' ')
    data = re.sub(' +', ' ', data)
    
    # Remove stop words
    stop_words = ['the', 'a', 'an', 'is', 'are', 'was', 'were', 'has', 'have', 'had', 'been', 'will', 'shall', 'be', 'to', 'of', 'and', 'in', 'that', 'for', 'on', 'with', 'by', 'at', 'from', 'as', 'into', 'through', 'during', 'including', 'until', 'against', 'among', 'throughout', 'despite', 'towards', 'upon']
    data = ' '.join([word for word in data.split() if word not in stop_words])
    
    # Remove all the words with length less than 3
    data = ' '.join([w for w in data.split() if len(w) > 2])
    
    # Remove all the filler words like 'like', 'uh', 'so', etc.
    filler_words = [
        'like', 'um', 'uh', 'ah', 'er', 'well', 'you know', 'actually', 'basically', 'literally',
        'honestly', 'seriously', 'right', 'so', 'anyway', 'anyhow', 'really', 'kind of', 'sort of',
        'pretty', 'quite', 'somewhat', 'just', 'still', 'now', 'can', 'this', 'all', 'make', 'there', 'then', 'therefore', 'thus', 'hence', 'its', 'you', 'thats'
    ]
    data = ' '.join([w for w in data.split() if w not in filler_words])
        
    return data

def main():
    document = []
    leetLength = 2000

    
    # Process data from leetcode source
    folder_path = f'./questionContent/'
    for filename in range(1, leetLength):
        try:    
            with open(folder_path + '/questionContentLeetcode' + str(filename) + ".txt", 'r', encoding="utf-8") as f:
                data = f.read()
                data = cleaningData(data)
                document.append(data)
        except:
            print(filename)

 # Continue with processing IDF and TF_IDF
    var = IDF(document)
    inverse_vocab_map = var[0]
    IDF_map = var[1]
    
    # by this we are storing the tf-idf values for each word in output.json
    TF_map = TF(document, inverse_vocab_map, IDF_map)
    
    # Continue with processing TF_IDF_map and saving output to 'output.json'
    TF_IDF_map = TF_IDF(TF_map, IDF_map)
    
    with open('output.json', 'w') as file:
        json.dump(TF_IDF_map, file)
        
    with open('doc.json', 'w') as file:
        json.dump(document, file)
        
    # storing document links and names
    document_links = []
    document_names = []

    targetDirectory = "./questionLinks/"
    length = len(os.listdir(targetDirectory))

    for i in range(1, leetLength):
        with open(targetDirectory + f'questionsLink_{i}.txt', encoding='utf-8') as f:
            data = f.read()
            document_links.append(data)
            f.close()
            
    targetDirectory = "./questionHeadings/"
    length = len(os.listdir(targetDirectory))         
            
    for i in range(1, leetLength):
        with open(targetDirectory + f'questionsName_{i}.txt', encoding='utf-8') as f:
            data = f.read()
            data = preprocess_name(data)
            document_names.append(data)
            f.close()
    
    # Save document links and names to 'links.json' and 'names.json', respectively
    with open('links.json', 'w') as file:
        json.dump(document_links, file)
        
    with open('names.json', 'w') as file:
        json.dump(document_names, file)

def TF_IDF(TF_map, IDF_map):
    # Calculate TF_IDF scores
    TF_IDF_map = {}
    
    for word in IDF_map:
        TF_IDF_map[word] = {}
        for index in TF_map[word]:
            TF_IDF_map[word][index] = TF_map[word][index] * IDF_map[word]
    
    return TF_IDF_map
    
def TF(document, inverse_vocab_map , IDF_map):
    # Calculate Term Frequency (TF) scores
    TF_map = {}
    
    for word in IDF_map:
        TF_map[word] = {}
        lst = inverse_vocab_map[word]
        
        for index in lst:
            para = document[index]
            para = para.split()
            if word in para:
                TF_map[word][index] = para.count(word) / len(para)
            else:
                TF_map[word][index] = 0
    
    return TF_map
    
def IDF(document):
    # Calculate Inverse Document Frequency (IDF) scores
    IDF_map = {}
    inverse_vocab_map = {}
    index = 0
    
    for para in document:
        para = set(para.split())
        for word in para:
            if word not in inverse_vocab_map:
                inverse_vocab_map[word] = []
            inverse_vocab_map[word].append(index)
            if word in IDF_map:
                IDF_map[word] += 1
            else:
                IDF_map[word] = 1
        index += 1
                
    for word in IDF_map:
        IDF_map[word] = 1 + math.log(len(document) / IDF_map[word])
        
    return inverse_vocab_map, IDF_map

if __name__ == "__main__":
    main()