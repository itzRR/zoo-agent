# 🦁 Zoo AI Assistant

A Google ADK-powered Zoo AI Assistant using **SequentialAgent** and the **Wikipedia tool**, deployed on **Google Cloud Run**.

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────┐
│         SequentialAgent         │
│  zoo_agent                      │
│                                 │
│  1. researcher  ──► wiki_tool   │
│         │                       │
│  2. formatter   ──► response    │
└─────────────────────────────────┘
```

- **Researcher Agent** — searches Wikipedia for factual info
- **Formatter Agent** — presents facts in a friendly, emoji-rich style
- **FastAPI** — REST API + built-in UI served at `/`

---

## 🚀 Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
# OR
uvicorn app:app --reload --port 8080
```

Open http://localhost:8080

---

## ☁️ Deploy to Google Cloud Run

### 1. Authenticate & Set Project

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Enable Required APIs

```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

### 3. Deploy

```bash
gcloud run deploy zoo-agent \
  --source . \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --port 8080
```

### 4. Test

```
# Health check
https://your-url.run.app/health

# Ask a question
https://your-url.run.app/ask?q=lion

# Open the UI
https://your-url.run.app/
```

---

## 🌐 API Endpoints

| Method | Endpoint   | Description                        |
|--------|------------|------------------------------------|
| GET    | `/`        | Zoo AI Assistant UI (HTML)         |
| GET    | `/health`  | Health check for Cloud Run         |
| GET    | `/ask?q=`  | Ask a question (JSON response)     |
| GET    | `/docs`    | Auto-generated Swagger/OpenAPI UI  |

### Example Response

```json
{
  "query": "lion",
  "response": "🦁 Lions are the second-largest big cats in the world! They live in sub-Saharan Africa and parts of India in grasslands and savannahs..."
}
```

---

## 📦 Project Structure

```
zoo-agent/
├── main.py           # Agent logic (SequentialAgent + wiki_tool)
├── app.py            # FastAPI app with built-in UI
├── requirements.txt  # Python dependencies
├── Dockerfile        # Cloud Run container
├── .dockerignore
└── README.md
```

---

## 🔑 Environment Variables

| Variable           | Description                        | Default |
|--------------------|------------------------------------|---------|
| `PORT`             | Port to listen on                  | `8080`  |
| `GOOGLE_CLOUD_PROJECT` | GCP project for Vertex AI      | —       |
