# Knowledge base generator

from pathlib import Path
import json

# set the path of the data source
DATA_SOURCE = Path("./tmdb/")

# Path for the chromaDB
CHROMADB_PATH = "./chromadb"

# ----------------------------------------------
# read the files from the data source directory
# ----------------------------------------------


# collect all the documents
documents = []

def load_documents():
    for document_path in DATA_SOURCE.glob("*.json"):
        
        # load the contents of the file
        with open(document_path, "r") as file:
            
            # load the json contents
            data = json.load(file)
            
            # collect the data
            documents.append(data)
        

load_documents()