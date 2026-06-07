# ⚖️ LexIntel AI

### Enterprise Legal Intelligence Platform Powered by Retrieval-Augmented Generation (RAG)

> Transforming legal research through semantic search, vector intelligence, and Large Language Models.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![LangChain](https://img.shields.io/badge/LangChain-RAG-orange)
![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-purple)
![Llama 3.3](https://img.shields.io/badge/Llama%203.3-LLM-red)
![Groq](https://img.shields.io/badge/Groq-Inference-black)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Quick Overview

LexIntel AI is an AI-powered legal research assistant that enables users to search, analyze, and understand legal documents using natural language.

Instead of relying on traditional keyword-based search, the platform uses Retrieval-Augmented Generation (RAG) to retrieve relevant legal information and generate context-aware responses grounded in document evidence.

---

## 🎯 Problem → Solution

### ❌ Problem

- Reading hundreds of pages of legal documents
- Searching through lengthy contracts manually
- Understanding complex legal terminology
- Locating specific clauses efficiently
- Time-consuming legal research workflows

### ✅ Solution

LexIntel AI enables users to:

- Ask questions in plain English
- Search legal documents semantically
- Retrieve relevant legal context instantly
- Generate source-grounded responses
- Reduce legal research time significantly

---

## 🌟 Key Highlights

- 🔍 Semantic Legal Search using Vector Embeddings
- 🤖 AI-Powered Legal Question Answering
- 📚 Retrieval-Augmented Generation (RAG)
- 🧠 Llama 3.3 Integration via Groq
- 🗄️ Pinecone Vector Database
- ⚡ FastAPI-Based Backend
- 🔐 Multi-Session Support
- 📄 Context-Aware Legal Knowledge Retrieval
- 🚀 End-to-End Generative AI Application

---

## 🏗️ Architecture Overview

```text
                    User Query
                         │
                         ▼
                Query Embedding
                         │
                         ▼
                 Pinecone Search
                         │
                         ▼
             Relevant Legal Chunks
                         │
                         ▼
                Context Injection
                         │
                         ▼
              Llama 3.3 via Groq
                         │
                         ▼
                 Generated Answer
```

---

## ✨ Features

### 🔍 Intelligent Legal Search
- Semantic search across legal documents
- Context-aware retrieval using vector embeddings
- Fast similarity-based document matching
- Meaning-based legal information discovery

### 🤖 AI-Powered Legal Assistant
- Natural language legal queries
- Contextual response generation
- Source-backed answers
- Conversational legal document exploration

### 📚 Retrieval-Augmented Generation
- Document chunking and indexing
- Embedding generation
- Retrieval-based response enhancement
- Context injection for improved answer accuracy

### ⚡ High Performance
- FastAPI backend architecture
- Optimized vector retrieval pipeline
- Concurrent request handling
- Scalable and modular design

### 🔐 Session Management
- Multi-user session support
- Query history tracking
- Session reset and cleanup functionality
- Isolated user conversations

---

## 🔄 End-to-End Workflow

```text
Legal Documents
      │
      ▼
Document Processing
      │
      ▼
Text Chunking
      │
      ▼
Embedding Generation
      │
      ▼
Pinecone Vector Database
      │
      ▼
Semantic Similarity Search
      │
      ▼
Relevant Context Retrieval
      │
      ▼
Llama 3.3 (Groq)
      │
      ▼
Context-Aware Legal Response
```

---

## 💡 Example Interaction

### User Query

```text
What are the termination conditions mentioned in this employment contract?
```

### Retrieved Context

```text
The employee may terminate the contract by providing a 30-day written notice.
Immediate termination is allowed in cases of misconduct or breach of obligations.
```

### AI Response

```text
According to the contract, either party can terminate the agreement by giving a 30-day written notice. The contract also permits immediate termination under specific circumstances such as misconduct or contractual violations.
```

---

## 🛠️ Technology Stack

| Category | Technology |
|-----------|-----------|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Frontend | Streamlit |
| Vector Database | Pinecone |
| Large Language Model | Llama 3.3 |
| Inference Engine | Groq |
| RAG Framework | LangChain |
| Embedding Pipeline | LangChain Embeddings |

---

## 📂 Project Structure

```text
LexIntel-AI/
│
├── data/
├── src/
│   ├── chatbot.py
│   ├── document_processor.py
│   ├── vector_store.py
│   ├── session_manager.py
│   ├── config.py
│   └── index_verification.py
│
├── app.py
├── document_uploader.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Installation & Setup

```bash
git clone https://github.com/yourusername/LexIntel-AI.git
cd LexIntel-AI

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### Environment Variables

```env
PINECONE_API_KEY=your_api_key
INDEX_NAME=your_index_name
GROQ_API_KEY=your_groq_api_key
```

---

## 📡 API Endpoints

| Endpoint | Method | Purpose |
|-----------|---------|---------|
| `/` | GET | Health Check |
| `/chat` | POST | Ask Legal Questions |
| `/session/reset/{session_id}` | POST | Reset Session |
| `/session/{session_id}` | DELETE | Delete Session |
| `/sessions/count` | GET | Active Sessions |
| `/sources/{session_id}` | GET | Retrieve Sources |

---

## 🎓 Skills Demonstrated

### Artificial Intelligence
- Generative AI
- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Prompt Engineering

### NLP & Information Retrieval
- Semantic Search
- Vector Similarity Search
- Context-Aware Question Answering
- Knowledge Retrieval Systems

### Software Engineering
- FastAPI Development
- REST API Design
- Session Management
- Modular Application Architecture

### Data Infrastructure
- Pinecone Vector Database
- Embedding Pipelines
- Vector Search Systems

---

## 🌟 Why This Project Matters

LexIntel AI demonstrates how modern AI systems can combine retrieval mechanisms with Large Language Models to produce trustworthy and context-aware responses.

The project showcases the practical implementation of RAG pipelines, vector databases, semantic search, and LLM-powered reasoning in a real-world legal research use case.

---

## 🔮 Future Roadmap

- 📄 PDF & DOCX Upload Support
- 📑 Citation Highlighting
- ⚖️ Legal Case Summarization
- 📚 Multi-Document Analysis
- 🧠 Conversational Memory
- 🔍 Hybrid Search (Keyword + Semantic)
- 📊 Analytics Dashboard
- 🌐 React Frontend

---

## 🏷️ GitHub Topics

```text
rag, llm, langchain, pinecone, legal-ai,
generative-ai, fastapi, streamlit,
semantic-search, vector-database, nlp
```

---

## 👨‍💻 Author

### Karthik Mekala

AI & Machine Learning Engineer

Building intelligent systems using Retrieval-Augmented Generation (RAG), Large Language Models, Generative AI, Vector Databases, Machine Learning, and Natural Language Processing.

⭐ If you found this project useful, consider giving it a star.
