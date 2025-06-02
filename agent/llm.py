from langchain_community.llms import Ollama
import json

llm = Ollama(model="gemma3:4b")

def get_intent(user_input):
    prompt = f"""
You are BitBud, the smartest function router. Based on the user message, return intent in **pure JSON**.

Your job is to understand the user’s intent and map it to the correct function.

**Only respond with JSON. No text. No explanations.**

Available functions:

- open_app(name: str)
- recommend_music()
- search_web(query: str)
- fallback()

### Rules:

1. Only use `open_app` if the user clearly says to open or launch an app (e.g., “open Spotify”, “launch VS Code”).
2. Only use `recommend_music` if the user explicitly asks for music suggestions or something like "recommend a song", "suggest music", etc. DO **NOT** use it for general conversation or vague requests.
3. Only use `search_web` if the user clearly asks to look something up, search online, or find information.
4. Use `fallback` for **ALL** other vague, conversational, or non-command messages (e.g., “My name is John”, “How are you?”, “This is great”, “Can you help?”, “I like pizza”).
5. Use **exactly** the function names and argument formats as shown below.

### Examples:

User: open Spotify  
→ {{ "function": "open_app", "args": {{ "name": "Spotify" }} }}

User: suggest me a good song  
→ {{ "function": "recommend_music" }}

User: look up weather in Tokyo  
→ {{ "function": "search_web", "args": {{ "query": "weather in Tokyo" }} }}

User: my name is Ayush  
→ {{ "function": "fallback", "args": {{}} }}

Now respond to this user message:

ALWAYS reply in pure JSON.

User: {user_input}
"""
    try:
        raw_response = llm.invoke(prompt).strip()
        print("[Raw LLM response]", raw_response)
        
        # Find JSON substring inside if the LLM adds fluff
        json_start = raw_response.find("{")
        json_end = raw_response.rfind("}") + 1
        json_block = raw_response[json_start:json_end]

        return json.loads(json_block)

    except Exception as e:
        print("[Intent parsing failed]", e)
        return {"function": "fallback", "args": {}, "error": str(e), "raw": raw_response}



    
# def summarize_memories(memories: list[str], query: str) -> str:
#     prompt = f"""
# You are an assistant with memory. You were asked: "{query}"

# You have access to the following memory snippets:
# {memories} entered by the user.
# Your task is to summarize these memories and provide a concise answer to the user's question.
# Only respond with information clearly found in these memories and write the answer as a reply to the user's question.
# Do not guess, infer, or make anything up. If nothing in the list helps answer the question, reply exactly:
# "I don't remember anything about that."
# """
#     res = requests.post("http://localhost:11434/api/generate", json={
#         "model": "gemma3:1b",
#         "prompt": prompt,
#         "stream": False
#     })

#     reply = res.json()["response"].strip()
#     print("Summarize Memories Result:", reply)
#     return reply
