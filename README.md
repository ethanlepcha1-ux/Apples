# KV Kalimpong Chatbot

A simple chatbot for **Kendriya Vidyalaya, Kalimpong** built with Python (Flask) and the Gemini API.

---

## 1. Install Dependencies

```bash
cd kv-chatbot
pip install -r requirements.txt
```

---

## 2. Add Your Gemini API Key

Open the `.env` file and replace `your_api_key_here` with your actual key:

```
GEMINI_API_KEY=your_api_key_here
```

> Get a free API key at [Google AI Studio](https://aistudio.google.com/apikey).

---

## 3. Run the App

```bash
python app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

---

## 4. Modifying the System Prompt / Personalization

Open [`app.py`](app.py) and look for the `SYSTEM_PROMPT` variable (around line 20).

It is a clearly sectioned multiline string. Edit the sections directly:

| Section | What to change |
|---|---|
| `CREATOR` | Your name, about you |
| `COLLABORATORS` | Names of teammates |
| `FRIENDS` | Info about your friends |
| `SCHOOL INFORMATION` | School details, timings, events, etc. |
| `BEHAVIOR` | How the chatbot should respond |

No database, no config files — just edit the string and restart the server.

---

## Project Structure

```
kv-chatbot/
├── app.py           ← Flask backend + system prompt (edit here)
├── .env             ← Your Gemini API key (never share this)
├── requirements.txt ← Python dependencies
├── templates/
│   └── index.html   ← Chat UI
└── README.md
```
