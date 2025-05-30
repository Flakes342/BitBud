import requests
import json

def get_intent(user_input):
    prompt = f"""
You are BitBud, the smartest function router. Based on this message, return intent in JSON.
The user will give you a command. You must decide what to do.


Respond with pure JSON only — never include explanations or extra text.

Available functions:

- open_app(name: str)
- recommend_music()
- search_web(query: str)
- remember(text: str)
- forget(text: str)

Important rules:
- For `remember`, always capture **everything after the word "remember"**, even if it's a full sentence.
- For `forget`, do the same — pass the full target phrase.
- For `recall`, always capture **everything after the word "remember"** and pass the full query user is trying to remember.
- Never modify or summarize user input — use it exactly.

Examples:

User: open <app-name> 
→ {{"function": "open_app", "args": {{"name": "<app-name>"}}}}

User: suggest me a good song  
→ {{"function": "recommend_music"}}

User: look up <search-query>  
→ {{"function": "search_web", "args": {{"query": "<search-query>"}}}}

User: remember <anything the user wants to save as memory>
→ {{"function": "remember", "args": {{"text": "<full memory content>"}}}}

User: forget <something previously remembered>  
→ {{"function": "forget", "args": {{"text": "<text-to-forget>"}}}}

User: recall <query to retrieve saved memory>  
→ {{"function": "recall", "args": {{"text": "<query-to-recall>"}}}}

Now respond to this user message:

ALWAYS reply in pure JSON and remember the output format!

User: {user_input}
"""
    # print("Prompt: ", prompt)
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    })

    # print ("Result: ", res)
    
    try:
        raw = res.json()["response"]
        json_start = raw.find("{")
        json_end = raw.rfind("}") + 1
        # print ("json_loads: ", raw[json_start:json_end])
        return json.loads(raw[json_start:json_end])
    except Exception as e:
        return {"function": "fallback", "args": {}, "error": str(e)}


    
def summarize_memories(memories: list[str], query: str) -> str:
    prompt = f"""
You are an assistant with memory. You were asked: "{query}"

You have access to the following memory snippets:
{memories} entered by the user.
Your task is to summarize these memories and provide a concise answer to the user's question.
Only respond with information clearly found in these memories and write the answer as a reply to the user's question.
Do not guess, infer, or make anything up. If nothing in the list helps answer the question, reply exactly:
"I don't remember anything about that."
"""
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False
    })

    reply = res.json()["response"].strip()
    print("Summarize Memories Result:", reply)
    return reply
