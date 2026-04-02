from fastapi import FastAPI
from pydantic import BaseModel
import os

from embeddings.embedder import get_embeddings
from vectorstore.faiss_store import load_vectorstore, create_and_save_vectorstore
from ingestion.loader import load_documents
from ingestion.chunking import split_documents

from rag.retriever import get_retriever
from rag.chain import create_rag_chain

from agents.tools import create_tools
from agents.agent import create_agent
from agents.memory import get_memory

from langchain_openai import ChatOpenAI
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI()

VECTOR_PATH = "faiss_index"


# 🔹 Request schema
class QueryRequest(BaseModel):
    query: str


# 🔹 GLOBAL OBJECTS (loaded once)
embeddings = get_embeddings()

if os.path.exists(VECTOR_PATH):
    logger.info("Loading existing vectorstore...")
    vectorstore = load_vectorstore(embeddings)
else:
    logger.info("Creating vectorstore...")
    docs = load_documents("data/sample.txt")
    chunks = split_documents(docs)
    vectorstore = create_and_save_vectorstore(chunks, embeddings)

retriever = get_retriever(vectorstore)
rag_chain = create_rag_chain(retriever)

llm = ChatOpenAI(model="gpt-4o-mini")
tools = create_tools(rag_chain, llm)

memory = get_memory()
agent = create_agent(tools, memory)


# 🔥 MAIN ENDPOINT
@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        response = agent.invoke({"input": request.query})
        return {
            "response": response["output"]
        }
    except Exception as e:
        logger.error("Error in chat endpoint", exc_info=True)
        return {"error": str(e)}