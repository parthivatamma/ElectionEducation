# AI Hackathon - Quick Start Guide

## 🚀 Getting Started

This guide will help you set up and run the AI Hackathon project locally.

## Prerequisites

- **Python 3.8+** with pip
- **Node.js 14+** with npm
- **Git**

## Backend Setup (FastAPI + RAG)

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:

- FastAPI & Uvicorn (web framework)
- LangChain (RAG framework)
- Sentence-Transformers (embeddings)
- FAISS (vector database)
- PyTorch (ML framework)

### Step 4: Run Backend Server

```bash
python main.py
```

Server will start at: **http://localhost:8000**

**API Documentation:** http://localhost:8000/docs (interactive Swagger UI)

## Frontend Setup (React)

### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Start Development Server

```bash
npm start
```

App will open at: **http://localhost:3000**

## Project Overview

### Backend Files

| File               | Purpose                                                     |
| ------------------ | ----------------------------------------------------------- |
| `main.py`          | FastAPI application with CORS and API endpoints             |
| `rag_engine.py`    | RAG engine using LangChain and FAISS for document retrieval |
| `scoring_algo.py`  | Article credibility scoring with weighted algorithm         |
| `requirements.txt` | Python dependencies                                         |

### Frontend Files

| File                               | Purpose                                         |
| ---------------------------------- | ----------------------------------------------- |
| `src/components/Questionnaire.jsx` | Dynamic onboarding questionnaire component      |
| `src/components/Questionnaire.css` | Component styling                               |
| `src/services/api.js`              | API utility functions for backend communication |
| `src/App.jsx`                      | Main app component                              |
| `public/index.html`                | HTML entry point                                |

## API Endpoints

### 1. Chat Endpoint

**URL:** `POST http://localhost:8000/api/chat`

**Request:**

```json
{
  "user_message": "What is machine learning?"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Message received",
  "response": "..."
}
```

**Frontend Usage:**

```javascript
import { sendChatMessage } from "./services/api";

const response = await sendChatMessage("What is AI?");
```

### 2. Scoring Endpoint

**URL:** `POST http://localhost:8000/api/score`

**Request:**

```json
{
  "article_url": "https://example.com/article"
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Article scoring initiated",
  "score": 75.5
}
```

**Frontend Usage:**

```javascript
import { getArticleScore } from "./services/api";

const result = await getArticleScore("https://example.com/article");
```

### 3. Health Check

**URL:** `GET http://localhost:8000/health`

**Frontend Usage:**

```javascript
import { checkAPIHealth } from "./services/api";

const health = await checkAPIHealth();
```

## Key Components

### Questionnaire Component

- **Location:** `frontend/src/components/Questionnaire.jsx`
- **Features:**
  - 4 sample onboarding questions
  - Progress bar tracking
  - Answer validation
  - Dynamic navigation
  - Submit functionality

**To modify questions**, edit the `questions` array in Questionnaire.jsx:

```javascript
const questions = [
  {
    id: 1,
    text: "Your question?",
    options: ["Option 1", "Option 2", "Option 3"],
  },
  // Add more questions...
];
```

### RAG Engine

- **Location:** `backend/rag_engine.py`
- **Usage:**

```python
from rag_engine import RAGEngine

# Initialize
rag = RAGEngine()

# Ingest documents
docs = ["Document 1...", "Document 2...", "Document 3..."]
rag.ingest_documents(docs)

# Query documents
prompt = rag.query_documents("What is Python?")
# Returns: "Answer the question using ONLY these documents. Documents: [...]. Question: What is Python?"
```

### Scoring Algorithm

- **Location:** `backend/scoring_algo.py`
- **Usage:**

```python
from scoring_algo import calculate_credibility_score

article_data = {
    "citation_count": 8,
    "has_author_credentials": True,
    "emotional_language_score": 0.2
}

score = calculate_credibility_score(article_data)  # Returns 0-100
```

**Score Calculation:**

- Citations: 40% weight
- Author Credentials: 30% weight
- Emotional Language (inverted): 30% weight

## Running Both Servers Simultaneously

### Terminal 1 (Backend):

```bash
cd backend
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
python main.py
```

### Terminal 2 (Frontend):

```bash
cd frontend
npm start
```

## Common Issues & Solutions

### Issue: Backend won't start

```
Error: ModuleNotFoundError: No module named 'fastapi'
```

**Solution:** Ensure virtual environment is activated and dependencies are installed

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: CORS error in browser console

**Error:** `Access to fetch at 'http://localhost:8000/api/chat' has been blocked by CORS policy`

**Solution:** Verify backend is running and has CORS middleware enabled in `main.py`

### Issue: Frontend won't start

```
Error: npm: command not found
```

**Solution:** Install Node.js from https://nodejs.org/

### Issue: Port already in use

```
Error: Port 8000 already in use
```

**Solution:** Kill process on port or change port in `main.py`

```bash
# macOS/Linux
lsof -i :8000
kill -9 <PID>

# Or change port in main.py: uvicorn.run(..., port=8001)
```

## Next Steps

1. **Integrate LLM:**
   - Add OpenAI API key or use local LLM
   - Modify `/api/chat` endpoint to use the LLM

2. **Add Chat UI:**
   - Create ChatWindow component in `frontend/src/components/`
   - Integrate with `sendChatMessage()` function

3. **Article Parsing:**
   - Fetch and parse article content
   - Extract citations and author info
   - Pass to `calculate_credibility_score()`

4. **Database:**
   - Add SQLAlchemy/PostgreSQL for data persistence
   - Store user responses, chat history, articles

## Useful Commands

### Backend

```bash
# Run with auto-reload (development)
uvicorn main:app --reload

# Run with specific port
uvicorn main:app --port 8001

# View API docs
# Visit: http://localhost:8000/docs
```

### Frontend

```bash
# Build for production
npm run build

# Run tests
npm test

# Eject configuration (⚠️ one-way operation)
npm run eject
```

## Project Structure

```
AIHackathon/
├── backend/
│   ├── main.py                    # FastAPI app
│   ├── rag_engine.py              # RAG implementation
│   ├── scoring_algo.py            # Scoring logic
│   └── requirements.txt           # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Questionnaire.jsx  # Questionnaire component
│   │   │   └── Questionnaire.css  # Styling
│   │   ├── services/
│   │   │   └── api.js             # API utilities
│   │   ├── App.jsx                # Main app
│   │   ├── index.js               # Entry point
│   │   └── index.css              # Global styles
│   ├── public/
│   │   └── index.html             # HTML template
│   ├── package.json               # Dependencies
│   └── .gitignore
├── .gitignore
├── README.md
└── QUICKSTART.md (this file)
```

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)

## Support

For issues or questions, check:

1. Error messages in terminal
2. Browser console (F12)
3. API docs at http://localhost:8000/docs
4. README.md for detailed information

---

**Happy coding! 🚀**
