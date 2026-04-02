def get_retriever(vectorstore):
    """
    Convert vector store into retriever
    """
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}  # top 3 chunks
    )
    
    return retriever