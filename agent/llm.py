from langchain_community.llms import Ollama
import json

llm = Ollama(model="gemma3:4b")

def get_intent(user_input):
    prompt = """
You are BitBud, the smartest function router. Based on the user message, return intent in **pure JSON**.

Your job is to understand the user’s intent and map it to the correct function.

**Only respond with JSON. No text. No explanations.**

Available functions:

- open_app(name: str, query: Optional[str])
- recommend_music()
- search_web(query: str)
- fallback()

### Rules:

1. Use `open_app` if the user clearly says to open or launch an app (e.g., “open Spotify”, “launch VS Code”).
   - If the user says something like “play *song name* on Spotify” or “open YouTube and search for *thing*”, include both `name` and `query`.
   - If they just say “open YouTube”, set `query` as "" or omit it.
2. Only use `recommend_music` if the user explicitly asks for music suggestions or something like "recommend a song", "suggest music", etc. DO **NOT** use it for general conversation or vague requests.
3. Only use `search_web` if the user **clearly asks** to look something up or search online. For example, “look up”, “search”, etc. DO **NOT** use it for general conversation or vague requests.
4. Use `fallback` for **ALL** other vague, conversational, or non-command messages (e.g., “My name is John”, “How are you?”, “This is great”, “Can you help?”, “I like pizza”).
5. Use **exactly** the function names and argument formats as shown below.

### Examples:

User: open Spotify  
→ {{ "function": "open_app", "args": { "name": "Spotify" } }}

User: play Espresso by Sabrina Carpenter on Spotify  
→ {{ "function": "open_app", "args": { "name": "Spotify", "query": "Espresso by Sabrina Carpenter" } }}

User: open YouTube and search lo-fi beats  
→ {{ "function": "open_app", "args": { "name": "YouTube", "query": "lo-fi beats" } }}

User: suggest me a good song  
→ {{ "function": "recommend_music" }}

User: look up weather in Gurugram  
→ {{ "function": "search_web", "args": {{ "query": "weather in Gurugram" }} }}

User: my name is Ayush  
→ {{ "function": "fallback", "args": {{}} }}

Now respond to this user message:

ALWAYS reply in pure JSON.

User: """ + user_input

    try:
        # print ("trying to parse intent from user input:", user_input)
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

# --- Prompt builder
def build_rag_prompt(user_input: str, context_docs: list[str]) -> str:
    context_str = "\n".join(context_docs)
    return f"""
You are BitBud, a concise and intelligent personal AI agent.

You have access to your following past conversations and memories with the user. 
{context_str}

Instruction:
Given the user input below, respond in a short, factual, and helpful way using the above context **only if it's relevant**. Do NOT guess or overexplain. If no context applies, respond naturally but **briefly**.

User: "{user_input}"
""".strip()


def generate_context_summary(text: str):
    prompt = f"""
You are a BitBud, a memory assistant.

Please generate a **short, high-quality contextual summary** of the user's message. The goal is to help retrieve this input later based on its intent, meaning, or relevance.

Focus on:
- The user’s **intent or fact stated** (e.g. they shared their name, asked a question, gave a command, made a preference known, etc.)
- Any **personal data** (like name, location, preferences)
- Any **task, question, or command** they gave
- Be **succinct, self-contained**, and only output the context.

Do **NOT** include generic statements like “The user said something” — instead be precise (e.g., “User shared their name is Ayush”).

Answer only with the cleaned-up, standalone context summary — no explanation, no prefixes.


Message: {text}
Summary:
"""
    summary = llm.invoke(prompt).strip()
    return None if summary.lower() == "none" else summary



