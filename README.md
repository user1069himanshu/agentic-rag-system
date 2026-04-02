# 🧠 Agentic RAG System (Multi-Tool AI Assistant)

An end-to-end **Agentic Retrieval-Augmented Generation (RAG)** system built using LangChain, FastAPI, and Redis, capable of dynamic tool selection, contextual reasoning, and multi-turn conversations.

---

## 🚀 Overview

This project implements a **production-style GenAI system** that combines:

- Retrieval-Augmented Generation (RAG)
- LLM-based decision-making (Agent)
- Multi-tool architecture (QA, summarization, calculator)
- Persistent memory using Redis
- FastAPI-based deployment layer

Unlike traditional RAG pipelines, this system introduces an **agentic reasoning layer**, enabling dynamic selection of tools based on query intent.

---

## 🧠 Key Features

- 🔍 **RAG Pipeline**
  - Document ingestion, chunking, embedding
  - FAISS-based vector retrieval
  - Context-aware answer generation

- 🤖 **Agentic AI Layer**
  - ReAct-based reasoning
  - Dynamic tool selection
  - Handles ambiguous queries intelligently

- 🧰 **Multi-Tool Support**
  - Document QA Tool (RAG)
  - Summarization Tool
  - Calculator Tool

- 🧠 **Persistent Memory (Redis)**
  - Multi-user chat sessions
  - Context retention across queries
  - Scalable architecture

- ⚡ **FastAPI Backend**
  - REST API for inference
  - Low-latency response handling

- 💾 **Optimized Pipeline**
  - Vectorstore persistence (FAISS)
  - Offline ingestion + online querying separation

---

## 🏗️ Architecture

User Query
    |
    v
FastAPI API
    |
    v
Agent (LLM Reasoning Layer)
    |
    v
Tools (RAG, Summarization etc)
    |
    v
Redis Memory (Chat History)
    |
    v
Response


---

## ⚙️ Tech Stack

- **LLM**: OpenAI (GPT-4o-mini)
- **Framework**: LangChain
- **Backend**: FastAPI
- **Vector DB**: FAISS
- **Memory**: Redis
- **Language**: Python

---

## 📂 Project Structure

agentic-rag-system/
├── app/
│   ├── api.py
│   ├── main.py
│   └── config.py
├── agents/
│   ├── agent.py
│   ├── memory.py
│   └── tools.py
├── embeddings/
│   └── embedder.py
├── ingestion/
│   ├── chunking.py
│   └── loader.py
├── rag/
│   ├── chain.py
│   └── retriever.py
├── vectorstore/
│   └── faiss_store.py
├── utils/
│   └── logger.py
├── data/
│   └── sample.txt
├── .env
├── requirements.txt
└── README.md
---

## ▶️ How to Run

### 1. Setup environment
```bash
python -m venv myvenv
myvenv\Scripts\activate
pip install -r requirements.txt