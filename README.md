Zoo AI Assistant

An intelligent multi-agent AI system powered by Gemini API, built using Google ADK, and deployed on Cloud Run.

--------------------------------------------------

OVERVIEW

Zoo AI Assistant is a cloud-based application that allows users to ask questions about animals and receive structured, AI-generated responses.

The system uses a SequentialAgent workflow:
- Researcher Agent → Generates answers using Gemini API
- Formatter Agent → Structures the response clearly

--------------------------------------------------

FEATURES

- Multi-agent architecture (SequentialAgent)
- Gemini-powered natural language responses
- Clean and interactive web UI
- Real-time query processing
- Cloud Run deployment (scalable & serverless)
- Secure API key handling via environment variables

--------------------------------------------------

TECH STACK

- Python
- FastAPI
- Google ADK (Agent Development Kit)
- Gemini API (Google AI)
- Docker
- Google Cloud Run

--------------------------------------------------

DEMO

Ask questions like:
Tell me about lions

The AI generates structured and informative responses with a clean UI.

--------------------------------------------------

SETUP (LOCAL)

1. Clone the repository
git clone https://github.com/your-username/zoo-agent.git
cd zoo-agent

2. Install dependencies
pip install -r requirements.txt

3. Set environment variable

Linux/Mac:
export GEMINI_API_KEY=your_api_key

Windows (PowerShell):
setx GEMINI_API_KEY "your_api_key"

4. Run locally
uvicorn app:app --reload

Open:
http://localhost:8000

--------------------------------------------------

DEPLOY TO CLOUD RUN

gcloud run deploy zoo-agent --source . --region asia-southeast1 --allow-unauthenticated --set-env-vars GEMINI_API_KEY=your_api_key

--------------------------------------------------

SECURITY NOTE

- Never expose your API key in code or GitHub
- Always use environment variables
- Regenerate keys if leaked

--------------------------------------------------

API ENDPOINTS

/           → Web UI
/ask?q=lion → Get AI response
/health     → Health check

--------------------------------------------------

USE CASE

- Educational AI assistant
- Animal knowledge system
- Multi-agent AI demonstration

--------------------------------------------------

AUTHOR

Rehan Bandara
Web Designer & Software Engineer

--------------------------------------------------

ACKNOWLEDGEMENTS

- Google Cloud
- Gemini API
- Google ADK

--------------------------------------------------

LICENSE

This project is for educational purposes.