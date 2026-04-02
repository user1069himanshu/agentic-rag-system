from langchain_openai import OpenAIEmbeddings


def get_embeddings():
    """
    Initialize embedding model
    """
    embeddings = OpenAIEmbeddings()
    return embeddings