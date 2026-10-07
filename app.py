import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT
# Edit this section to change the chatbot's personality and personalization.
# ──────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are the Kendriya Vidyalaya Assistant.
Your job is to help answer questions related to Kendriya Vidyalaya, Kalimpong,
its academics, campus, students, activities, rules, schedules, facilities,
and other school-related topics.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PERSONALIZATION
Use the following information only when it is relevant to the conversation.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATOR
This chatbot was created by Ethan, a student at Kendriya Vidyalaya, Kalimpong.

COLLABORATORS
Ethan built this chatbot with the help of:
- Ethan
- Nityasha
- Kamlesh

FRIENDS
[Add information about friends here when needed.]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCHOOL INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

School Name: Kendriya Vidyalaya, Kalimpong
Location: Kalimpong, West Bengal, India
Type: Central Government School (KV)

[Add more specific school details here as needed — timings, principal name,
 events, clubs, house system, etc.]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCHOOL CLUBS 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
There are many clubs in the school .
Most popular ones are : The Reader's Club , KV KPG CHESS CLUB , Hunter's Hike Club 

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEHAVIOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Be helpful, friendly, and conversational.
- Be respectful and use simple words .
- Keep answers clear and easy to understand.
- Do NOT invent or make up information about Kendriya Vidyalaya, Kalimpong.
- If you do not know something specific, say so honestly rather than guessing.
- Use the personalization information naturally — don't mention it unnecessarily.
- Answer the user's actual question directly without unnecessary filler.
- Keep responses concise unless the user asks for detail.
"""

# ──────────────────────────────────────────────────────────────────────────────
# Gemini Setup
# The client is created lazily inside the route so Vercel doesn't crash
# during the build phase before environment variables are injected.
# ──────────────────────────────────────────────────────────────────────────────

MODEL_NAME = "gemini-2.0-flash"

def get_client():
    """Return a Gemini client, raising a clear error if the key is missing."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. "
            "Add it to your .env file locally, or to Vercel's Environment Variables."
        )
    return genai.Client(api_key=api_key)

# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the chat UI."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Receive message + conversation history from the frontend,
    send to Gemini, and return the reply.

    Expected JSON body:
    {
        "message": "user's latest message",
        "history": [
            {"role": "user", "parts": ["..."]},
            {"role": "model", "parts": ["..."]}
        ]
    }
    """
    data = request.get_json()

    user_message = data.get("message", "").strip()
    history = data.get("history", [])  # list of {role, parts} dicts

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        client = get_client()

        # Convert history to the format the new SDK expects
        formatted_history = [
            types.Content(
                role=turn["role"],
                parts=[types.Part(text=p) for p in turn["parts"]],
            )
            for turn in history
        ]

        # Send message with full conversation history and system prompt
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=formatted_history + [
                types.Content(role="user", parts=[types.Part(text=user_message)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )

        return jsonify({"reply": response.text})

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Something went wrong. Please try again."}), 500


# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # debug=False in production; Vercel handles this automatically
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
