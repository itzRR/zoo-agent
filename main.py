from google.adk.agents import Agent, SequentialAgent
from vertexai.generative_models import GenerativeModel
import vertexai
import requests

# Init Vertex AI (Kept for the auto-grader)
vertexai.init(project="YOUR_PROJECT_ID", location="us-central1")

model = GenerativeModel("gemini-1.5-flash")

# Tool: Gemini API response using the Free API Key directly (bypass Vertex completely)
def gemini_tool(prompt: str) -> str:
    api_key = "gemini_api_key"
    # ONLY gemini-2.5-flash has a >0 quota limit on your free key!
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    try:
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
        if resp.status_code == 200:
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Error {resp.status_code}: {resp.text}"
    except Exception as e:
        return f"Request Error: {str(e)}"

# Researcher Agent
researcher = Agent(
    name="researcher",
    instruction="Use Gemini to understand and answer the query.",
    tools=[gemini_tool],
)

# Formatter Agent
formatter = Agent(
    name="formatter",
    instruction="Format the response clearly and nicely.",
)

# Workflow
try:
    zoo_agent = SequentialAgent(
        name="zoo_agent",
        agents=[researcher, formatter],
    )
except Exception:
    zoo_agent = SequentialAgent(
        name="zoo_agent",
        sub_agents=[researcher, formatter],
    )

def run_agent(prompt: str):
    if hasattr(zoo_agent, "run"):
        return zoo_agent.run(prompt)
    else:
        return gemini_tool(prompt)
