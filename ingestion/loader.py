from langchain_community.document_loaders import TextLoader


def load_documents(file_path: str):
    """
    Load documents from a text file
    """
    loader = TextLoader(file_path)
    documents = loader.load()
    
    return documents