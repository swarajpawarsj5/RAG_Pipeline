# read data by langchain document loaders

from langchain_community.document_loaders import TextLoader,PyMuPDFLoader

def load_text_file(file_name: str):
    
    # create the TextLoader
    loader = TextLoader(file_path=file_name)
    
    # Load the text data
    data = loader.load()
    print(data)
    
load_text_file("./data/sample.txt")
    
def load_pdf_file(file_name: str):
    
    # create the TextLoader
    loader = PyMuPDFLoader(file_path=file_name)
    
    # Load the text data
    data = loader.load()
    print(data)
    


# load_pdf_file("./data/swaraj_resume.pdf")