# Autonomous Multi-Agent AI System with RAG and FastAPI

## 🚀 Overview

This project is a production-style Autonomous Multi-Agent AI System built using FastAPI, LLMs, Retrieval-Augmented Generation (RAG), vector search, and dynamic tool orchestration.

The system can:

- Break complex queries into subtasks
- Use multiple AI agents for execution
- Retrieve knowledge from uploaded documents using RAG
- Perform real-time web search
- Maintain session-based conversational memory
- Provide explainable reasoning and source citations
- Support multiple uploaded documents per session

---

## 🧠 Core Features

### ✅ Multi-Agent Architecture
- Planner Agent
- Executor Agent
- Tool Selection Agent
- Retrieval Agent

### ✅ Retrieval-Augmented Generation (RAG)
- PDF/DOCX/TXT upload
- Text chunking
- Embedding generation
- FAISS vector search
- Session-based document isolation
- Multi-document support

### ✅ Dynamic Tool Selection
The system uses an LLM to dynamically decide:
- Web Search
- RAG Retrieval
- General LLM Reasoning

### ✅ Explainable AI
Each response includes:
- Tool used
- Reason for selection
- Agent reasoning steps
- Retrieved document sources

### ✅ Real-Time Web Search
Integrated with Tavily API for live external information retrieval.

### ✅ Session Memory
Maintains previous conversation context using MySQL.

---

## 🏗️ Tech Stack

### Backend
- FastAPI
- Python

### AI / ML
- Groq LLM API
- Sentence Transformers
- RAG Pipeline
- FAISS Vector Database

### Database
- MySQL
- SQLAlchemy ORM

### Tools
- Tavily Web Search API

### Frontend
- HTML
- CSS
- JavaScript

---

## 📂 Project Structure

```bash
app/
│
├── agents/
│   ├── planner.py
│   └── executor.py
│
├── api/
│   └── v1/
│       └── endpoints/
│           ├── query.py
│           └── upload.py
│
├── core/
│   ├── config.py
│   ├── database.py
│   └── logger.py
│
├── models/
│   ├── db_models.py
│   └── request_models.py
│
├── orchestrator/
│   └── workflow.py
│
├── rag/
│   ├── embeddings.py
│   ├── retriever.py
│   └── vector_store.py
│
├── services/
│   ├── db_service.py
│   └── llm_service.py
│
├── static/
│   └── index.html
│
├── tools/
│   ├── tool_selector.py
│   └── web_search.py
│
└── main.py