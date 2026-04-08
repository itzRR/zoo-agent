import os
import requests

print("🚀 Zoo Agent starting...")

# 🔹 Gemini API Tool
def gemini_tool(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Error: API key not found."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    try:
        response = requests.post(
            url,
            json={
                "contents": [
                    {"parts": [{"text": prompt}]}
                ]
            },
            timeout=20
        )

        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"API Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Request Error: {str(e)}"


# 🔹 Try to load ADK (safe)
try:
    from google.adk.agents import Agent, SequentialAgent

    researcher = Agent(
        name="researcher",
        instruction="Understand the query and answer clearly using Gemini.",
        tools=[gemini_tool],
    )

    formatter = Agent(
        name="formatter",
        instruction="Format the response clearly using bullet points or short paragraphs.",
    )

    # Handle ADK version differences
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

    print("✅ ADK loaded successfully")

except Exception as e:
    print("⚠️ ADK failed, using fallback:", e)
    zoo_agent = None


# 🔹 Run function (FINAL SAFE VERSION)
def run_agent(prompt: str):
    try:
        if zoo_agent:
            if hasattr(zoo_agent, "run"):
                return zoo_agent.run(prompt)
            elif hasattr(zoo_agent, "invoke"):
                return zoo_agent.invoke(prompt)
        
        # fallback (always works)
        return gemini_tool(prompt)

    except Exception as e:
        return f"Agent Error: {str(e)}"