from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


def create_rag_chain(retriever):
    """
    Modern RAG pipeline (LangChain v1)
    """

    llm = ChatOpenAI(model="gpt-4o-mini")

    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer based only on the provided context:\n\n{context}"),
        ("human", "{input}")
    ])

    # Combine docs chain
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Final RAG chain
    rag_chain = create_retrieval_chain(retriever, document_chain)

    return rag_chain