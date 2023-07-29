from flask import Flask, jsonify
import math
import re
import os
import json
import sys
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key' 

if __name__ == '__main__':
    # try:
    # Get the current directory of the script
    current_dir = os.curdir

    # Load TF-IDF map, document links, document names, and document from their respective JSON files
    output_file = os.path.join(current_dir, 'output.json')
    doc_file = os.path.join(current_dir, 'doc.json')
    links_file = os.path.join(current_dir, 'links.json')
    names_file = os.path.join(current_dir, 'names.json')
    
    with open(output_file, 'r') as file:
        TF_IDF_map = json.load(file)

    with open(doc_file, 'r') as file:
        document = json.load(file)
    
    with open(links_file, 'r') as file:
        document_links = json.load(file)

    with open(names_file, 'r') as file:
        document_names = json.load(file)



def main(TF_IDF_map, document_links, document_names, document,query):
    # Get the query from the command-line argument or ask the user to input it
    # if len(sys.argv) > 1:
    #     query = sys.argv[1]
    # else:
    #     query = input("Enter your query: ")
        
    # Preprocess the query: lowercase and split into individual words
    query = query.lower()
    query = query.split()

    # Dictionary to store potential documents and their corresponding TF-IDF scores
    potential_documents = {}
    results = []

    try:
        # Match the query terms against the TF-IDF map to find relevant documents
        for word in query:
            if word in TF_IDF_map:
                for index in TF_IDF_map[word]:
                    if index in potential_documents:
                        potential_documents[index] += TF_IDF_map[word][index]
                    else:
                        potential_documents[index] = TF_IDF_map[word][index]
                        
        # Sort the potential documents based on their TF-IDF scores in descending order
        potential_documents = sorted(potential_documents.items(), key=lambda x: x[1], reverse=True)

        # Create a list of search results containing document links and names
        for index , score in potential_documents:
            index = int(index)
            results.append(str(document_links[index]) + "*" + str(document_names[index]))
    except Exception as e:
        print("An error occurred:", e)
        exit()
        
    # Ensure uniqueness in the search results by converting them into a set and then back to a list
    results = list(set(results))
        
    # Create an output data dictionary containing the search results
    output_data = {
        'results': results
    }

    # Convert the output data to JSON string
    json_data = json.dumps(output_data)

    return json_data



class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')


@app.route("/<query>")
def return_links(query):
    # q_terms = [term.lower() for term in query.strip().split()]
    results = main(TF_IDF_map, document_links, document_names, document,query)
    return results


@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search.data
        results = main(TF_IDF_map, document_links, document_names, document,query)
    return render_template('index.html', form=form, results=results)
# flask (backend)




    


    # Print the JSON data, which contains the search results, to the console
    # print(json_data)


# flask (backend)


    

    # except:
    #     exit()
        
    # Call the main function with the loaded data to perform the search and display the results
    # main(TF_IDF_map, document_links, document_names, document)
app.run(debug=True)



