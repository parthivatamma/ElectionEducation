# ElectionEducation

A full-stack application combining a FastAPI backend with RAG (Retrieval-Augmented Generation) capabilities and a React frontend for article credibility assessment and intelligent chat interactions.

## Project Structure

```
AIHackathon/
├── backend/
│   ├── main.py                 # FastAPI application with CORS and endpoints
│   ├── rag_engine.py           # RAG engine using LangChain and FAISS
│   ├── scoring_algo.py         # Article credibility scoring algorithm
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Questionnaire.jsx     # Onboarding questionnaire component
│   │   │   └── Questionnaire.css     # Component styling
│   │   └── services/
│   │       └── api.js          # API utility functions
│   ├── public/
│   ├── package.json
│   └── .gitignore
└── README.md
```

## Backend Setup

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

1. **Navigate to backend directory:**

   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Backend

```bash
python main.py
```

The API will be available at `http://localhost:8000`

**API Documentation:** Visit `http://localhost:8000/docs` (Swagger UI)

### Backend Components

#### 1. **main.py** - FastAPI Application

- CORS middleware configured for localhost:3000
- `/api/chat` - POST endpoint for chat messages
- `/api/score` - POST endpoint for article scoring
- `/health` - Health check endpoint

#### 2. **scoring_algo.py** - Credibility Scoring

Function: `calculate_credibility_score(article_data: dict) -> float`

Weights:

- Citation count: 40%
- Author credentials: 30%
- Emotional language score: 30% (inverted)

Example usage:

```python
from scoring_algo import calculate_credibility_score

article = {
    "citation_count": 8,
    "has_author_credentials": True,
    "emotional_language_score": 0.2
}

score = calculate_credibility_score(article)  # Returns 0-100
```

#### 3. **rag_engine.py** - RAG Engine

Class: `RAGEngine`

Methods:

- `ingest_documents(docs: List[str])` - Embed and store documents
- `query_documents(user_query: str, top_k: int = 3) -> str` - Retrieve relevant documents and format prompt

Example usage:

```python
from rag_engine import RAGEngine

rag = RAGEngine()
docs = ["Doc1...", "Doc2...", "Doc3..."]
rag.ingest_documents(docs)

prompt = rag.query_documents("What is Python?")
print(prompt)  # Returns formatted prompt with retrieved documents
```

## Frontend Setup

### Prerequisites

- Node.js 14+
- npm or yarn

### Installation

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

### Running the Frontend

```bash
npm start
```

The app will open at `http://localhost:3000`

### Frontend Components

#### 1. **Questionnaire.jsx** - Onboarding Form

- Dynamic questionnaire with 4 sample questions
- Answer tracking with `userAnswers` state
- Progress bar and navigation
- Submit functionality

Features:

- Previous/Next navigation
- Selected state for answers
- Progress indicator
- Submit button (shows when all questions answered)

#### 2. **api.js** - API Utilities

Functions:

- `sendChatMessage(message)` - Send chat message to backend
- `getArticleScore(url)` - Get article credibility score
- `checkAPIHealth()` - Health check
- `sendQuestionnaire(answers)` - Send questionnaire responses

Example usage:

```javascript
import { sendChatMessage, getArticleScore } from "./services/api";

// Send chat message
const response = await sendChatMessage("Hello!");
console.log(response.data);

// Get article score
const score = await getArticleScore("https://example.com/article");
console.log(score.score);
```

## API Endpoints

### Chat Endpoint

**POST** `/api/chat`

Request:

```json
{
  "user_message": "Your question here"
}
```

Response:

```json
{
  "status": "success",
  "message": "Message received",
  "response": "Processed message: '...' (RAG integration pending)"
}
```

### Scoring Endpoint

**POST** `/api/score`

Request:

```json
{
  "article_url": "https://example.com/article"
}
```

Response:

```json
{
  "status": "success",
  "message": "Article scoring initiated",
  "score": 75.0
}
```

## Integration Guide

### Connecting Frontend to Backend

1. Ensure backend is running on `http://localhost:8000`
2. The frontend API utilities in `services/api.js` are configured to connect to this URL
3. Use the provided utility functions in components:

```javascript
import { sendChatMessage } from "./services/api";

// In your React component
const handleSendMessage = async () => {
  try {
    const result = await sendChatMessage(userMessage);
    console.log("Chat response:", result);
  } catch (error) {
    console.error("Error:", error);
  }
};
```

### Integrating RAG Engine

The RAG engine is ready in `backend/rag_engine.py`. To integrate with the chat endpoint:

1. Import RAGEngine in main.py
2. Initialize on application startup
3. Call `query_documents()` in the `/api/chat` endpoint
4. Pass the prompt to your LLM

```python
from rag_engine import RAGEngine

rag = RAGEngine()
# Ingest your documents
rag.ingest_documents(your_documents)

# In /api/chat endpoint
prompt = rag.query_documents(user_message)
# Then call your LLM with this prompt
```

### Integrating Scoring Algorithm

Use in the `/api/score` endpoint to calculate credibility scores:

```python
from scoring_algo import calculate_credibility_score

# After extracting article data
score = calculate_credibility_score({
    "citation_count": count,
    "has_author_credentials": bool_value,
    "emotional_language_score": float_value
})
```

## Next Steps

1. **Backend Enhancement:**
   - Integrate with a real LLM API (OpenAI, HuggingFace, etc.)
   - Add document ingestion/parsing endpoints
   - Implement article fetching and parsing

2. **Frontend Enhancement:**
   - Add chat interface component
   - Implement article URL input form
   - Add result visualization
   - Error handling and loading states

3. **Database:**
   - Add persistent storage for user data
   - Store chat history
   - Cache embeddings

## Dependencies

### Backend

- FastAPI
- Uvicorn
- LangChain
- Sentence-Transformers
- FAISS
- PyTorch

### Frontend

- React
- Fetch API (built-in)

## Notes

- The scoring algorithm uses a weighted sum approach suitable for production use
- FAISS vector store is lightweight and suitable for local development
- For production, consider using FAISS-GPU or cloud vector databases
- Customize the RAG engine model by changing the `model_name` parameter in RAGEngine.**init**()

## Troubleshooting

**Backend not connecting:**

- Ensure backend is running on port 8000
- Check CORS configuration in main.py
- Verify `http://localhost:8000` is accessible

**RAG engine failing:**

- Ensure sentence-transformers and FAISS are properly installed
- Try reinstalling with: `pip install --upgrade sentence-transformers faiss-cpu`

**Frontend API errors:**

- Check browser console for error messages
- Verify API endpoint URLs in `services/api.js`
- Use the `/health` endpoint to verify API is running

## License

MIT License

## Authors

AI Hackathon Team
