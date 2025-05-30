import requests
import json
import subprocess

def process_message(message):
    decision = get_llm_function_call(message)

    # plain string
    if isinstance(decision, str):
        return decision

    # reply-only response
    if "reply" in decision:
        return decision["reply"]

    # function call
    function = decision.get("function")
    args = decision.get("args", {})

    # string-encoded args like "query=xyz"
    if isinstance(args, str):
        parts = args.split("=")
        if len(parts) == 2:
            args = {parts[0].strip(): parts[1].strip()}
        else:
            args = {}

    if function == "open_app":
        return open_app(args.get("name", "unknown"))
    elif function == "search_web":
        return search_web(args.get("query", "unknown"))
    elif function == "recommend_music":
        return recommend_music()

    return "Sorry, I didn’t understand that."


def get_llm_function_call(message):
    prompt = f"""
You are DOT, a helpful AI agent for a Linux desktop. 
The user will give you a command. You must decide what to do.

You can:
1. Open apps on the desktop
2. Recommend music
3. Search the web (just say you'll search)

Respond with pure JSON only — never include explanations or extra text.

Available functions:

- open_app(name: str)
- recommend_music()
- search_web(query: str)

Examples:

User: open spotify  
→ {{"function": "open_app", "args": {{"name": "spotify"}}}}

User: suggest me a good song  
→ {{"function": "recommend_music"}}

User: look up quantum physics  
→ {{"function": "search_web", "args": {{"query": "quantum physics"}}}}

Now respond to this user message:
User: {message}
"""


    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma3:1b", "prompt": prompt, "stream": False}
        )
        raw = res.json().get("response", "").strip()
        print ("Raw: ",raw)

        # Cleaning any stray text before/after JSON
        json_start = raw.find("{")
        json_end = raw.rfind("}") + 1
        cleaned = raw[json_start:json_end]


        return json.loads(cleaned)

    except Exception as e:
        return {"reply": f"LLM error: {str(e)}"}


def open_app(app_name):
    print (f"Opening app: {app_name}")
    app_commands = {
        "spotify": "spotify",
        "vscode": "code",
        "youtube": "firefox https://youtube.com",
        "netflix": "firefox https://netflix.com",
        "chrome": "google-chrome",
        "terminal": "gnome-terminal",
    }

    command = app_commands.get(app_name.lower())
    if command:
        try:
            subprocess.Popen(command.split())
            return f"Opening {app_name}."
        except Exception as e:
            return f"Failed to open {app_name}: {e}"
    else:
        return f"I don't know how to open '{app_name}' yet."

def recommend_music():
    return "Try 'Mare Yuvraj sa Chakka'."

def search_web(query):
    return f"Searching the web for: {query}...khikhi, I can't do that yet."

