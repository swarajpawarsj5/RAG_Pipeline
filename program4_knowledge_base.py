# knowledge base generator
# pip install chromadb langchain-chroma

from pathlib import Path
import json

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# set the path of the data source
DATA_SOURCE = Path("./tmdb/")

# path for the chromaDB
CHROMA_DB_PATH = "./chromadb"

# ----------------------------------------------
# create the chroma store
# ----------------------------------------------

# create embeddings function for embedding conversion
embedding_function = OllamaEmbeddings(model="nomic-embed-text")

chroma = Chroma(
    # collection name (similar to the table in RDBMS)
    collection_name="movies",

    # path of the vector store
    persist_directory=CHROMA_DB_PATH,

    # embedding function is used to convert the data into embeddings
    embedding_function=embedding_function
)

# ----------------------------------------------
# read the files from the data source directory
# ----------------------------------------------

# collect all the documents
documents = []

# function to create a movie document
def create_movie_document(data):

    # get the movie from the data
    movie = data['movie']

    # get the movie information
    title = movie['title']
    overview = movie['overview']
    status = movie['status']
    genres = ', '.join([genre['name'] for genre in movie.get('genres', [])])
    cast = ', '.join([actor['name'] for actor in data.get('cast', [])])
    keywords = ', '.join([keyword['name'] for keyword in data.get('keywords', [])])
    recommendations = ', '.join([recommendation['title'] for recommendation in data.get('recommendations', [])])

    # filter the director info
    directors = []
    for member in data.get('crew', []):
        if member['job'] == 'Director':
            directors.append(member['name'])

    # club all the extracted information to create a single document for every movie
    movie_document = f"""
Title: {title}

Overview: {overview}

Status: {status}

Genres: {genres}

Cast: {cast}

Keywords: {keywords}

Recommendations: {recommendations}

Directors: {', '.join(directors)}
"""

    # add the metadata for the movie
    metadata = {
        "movie_id": movie['id'],
        "title": movie['title'],
        "language": movie['original_language'],
        "director": ', '.join(directors),
        "poster": movie['poster_path'],
        "genres": genres,
        "keywords": keywords,
        "overview": overview
    }

    # convert the movie document in Document format to get inserted into chroma db
    return Document(
        page_content=movie_document.strip(),
        metadata=metadata
    )
    

# file counter
index = 1

for document_path in DATA_SOURCE.glob("*.json"):

    print(f"opening and creating document no: {index}")

    # load the contents of the file
    with open(document_path, "r" , encoding="utf-8") as file:

        # load the json contents
        data = json.load(file)

        # collect the data
        movie_document = create_movie_document(data)
        documents.append(movie_document)

        # add the documents to the chroma db
        chroma.add_documents([movie_document])

    index += 1

print("knowledge base is ready...")