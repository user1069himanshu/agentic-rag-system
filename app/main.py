from ingestion.loader import load_documents
from ingestion.chunking import split_documents
from app.config import OPENAI_API_KEY
from embeddings.embedder import get_embeddings
from vectorstore.faiss_store import create_vector_store

from rag.retriever import get_retriever
from rag.chain import create_rag_chain


def main():
    docs = load_documents("data/sample.txt")
    chunks = split_documents(docs)

    embeddings = get_embeddings()
    vectorstore = create_vector_store(chunks, embeddings)

    retriever = get_retriever(vectorstore)
    rag_chain = create_rag_chain(retriever)

    print("\n💬 Ask something (type 'exit' to quit):")

    while True:
        query = input(">> ")

        if query.lower() == "exit":
            break

        response = rag_chain.invoke({"input": query})
        print("\n🤖 Answer:", response["answer"], "\n")


if __name__ == "__main__":
    main()