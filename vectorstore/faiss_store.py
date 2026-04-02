from langchain_community.vectorstores import FAISS


def create_and_save_vectorstore(chunks, embeddings, path="faiss_index"):
    """
    Create and persist FAISS vector store
    """
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(path)
    return vectorstore


def load_vectorstore(embeddings, path="faiss_index"):
    """
    Load FAISS vector store from disk
    """
    vectorstore = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    return vectorstore