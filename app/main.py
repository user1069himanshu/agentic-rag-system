from langchain_openai import ChatOpenAI

from ingestion.loader import load_documents
from ingestion.chunking import split_documents

from app.config import OPENAI_API_KEY

from embeddings.embedder import get_embeddings

from vectorstore.faiss_store import create_and_save_vectorstore, load_vectorstore
VECTOR_PATH = "faiss_index"

from rag.retriever import get_retriever
from rag.chain import create_rag_chain

from agents.tools import create_tools
from agents.agent import create_agent

from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    llm = ChatOpenAI(model="gpt-4o-mini")

    embeddings = get_embeddings()

    if os.path.exists(VECTOR_PATH):
        logger.info("Loading existing vectorstore...")
        vectorstore = load_vectorstore(embeddings, VECTOR_PATH)
        logger.debug("vectorstore loaded : %s", vectorstore)
    else:
        logger.info("Creating new vectorstore...")
        docs = load_documents("data/sample.txt")
        chunks = split_documents(docs)
        logger.debug("chunks created : %d, length of chunks : %d", len(chunks), len(chunks[0]))
        vectorstore = create_and_save_vectorstore(chunks, embeddings)

    retriever = get_retriever(vectorstore)
    rag_chain = create_rag_chain(retriever)

    tools = create_tools(rag_chain, llm)
    agent = create_agent(tools)

    logger.info("\n💬 Ask something (type 'exit' to quit):")

    while True:
        query = input(">> ")

        if query.lower() == "exit":
            break

        response = agent.run(query)
        logger.info("\n🔥 Final Answer:", response, "\n")


if __name__ == "__main__":
    main()