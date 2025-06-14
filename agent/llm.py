from langchain_community.llms import Ollama
from typing import Optional, TypedDict
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
- linux_commands(command: str)
- clock(type: str, hour: Optional[int], minute: Optional[int], seconds: Optional[int], objective: Optional[str])
- system_control(type: str)

- fallback()

### Rules:

1. Use `open_app` if the user clearly says to open or launch an app (e.g., “open Spotify”, “launch VS Code”).
   - If the user says something like “play *song name* on Spotify” or “open YouTube and search for *thing*”, include both `name` and `query`.
   - If they just say “open YouTube”, set `query` as "" or omit it.
2. Only use `recommend_music` if the user explicitly asks for music suggestions or something like "recommend a song", "suggest music", etc. DO **NOT** use it for general conversation or vague requests.
3. Only use `search_web` if the user **clearly asks** to look something up, search online, or find information. For example, uch as “look up”, “search online”, “Google”, “find on web”, or “get info about X online”. DO **NOT** use it for general conversation, memeory based requests, vague requests or when user asks something that can be answered by the agent's memory.
4. Use `run_linux_command` if the user asks for a specific shell command or task that can be done via terminal (e.g., “run ls -l”, “show current directory”, etc.). DO **NOT** use it for general conversation or vague requests.
5. Use `clock` for any time-related task:
   - Alarm: “set alarm for 6:30” → `type: "alarm", hour, minute, objective`
   - Timer: “start a 10-minute timer” → `type: "timer", seconds, objective`
   - Current time: “what time is it?” → `type: "get_time"`
   - List alarms: “list all alarms” → `type: "get_active_alarms"`
   - List timers: “list all timers” → `type: "get_active_timers"`
   - Clear alarms: “clear all alarms” → `type: "clear_alarms"`
   - Clear timers: “clear all timers” → `type: "clear_timers"`
6. Use `system_control` for any system-related tasks for example, “get system info”, "get system temperature", “list running processes”, "kill a proceess", "abort a job", "current volume","set volume to 10%","increase volume", "decrease volume by 10%", "immediate actions like shutdown, logout, sleep", etc. Be very careful with shutdown, restart, logout, sleep, hibernate commands as they will immediately affect the system.
7. Use `fallback` for **ALL** other vague, conversational, non-command messages, memory based, user asking questions about them and their life (e.g., “My name is John”, “How are you?”, “This is great”, “Can you help?”, “I like pizza”, "What is my..?").
8. You have an ABOUT.md file that contains information about the user. If the user asks something that can be answered by the agent's memory, use the `fallback` function to retrieve the information from the memory and return it as a response.
9. Use **exactly** the function names and argument formats as shown below. Always use the correct function name and argument structure.

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

User: run a command to do something in terminal  
→ {{ "function": "linux_commands", "args": {"command": "<bash-comamnd>"} }}

User: What time is it? 
→ {{ "function": "clock", "args": {{ "type": "get_time"}} }}

User: I want to take some break, set a timer for 10 minutes 
→ {{ "function": "clock", "args": {{ "type": "timer", "seconds": 600, "objective": "break time" }} }}

User: set alarm for 6:30 AM to wake up
→ {{ "function": "clock", "args": {{ "type": "alarm", "hour": 6, "minute": 30, "objective": "wake up" }} }}

User: list all alarms / get alarms / what alarms do I have?
→ {{ "function": "clock", "args": {{ "type": "get_active_alarms" }} }}

User: list all timers / get timers / what timers do I have?
→ {{ "function": "clock", "args": {{ "type": "get_active_timers" }} }}

User: clear all alarms
→ {{ "function": "clock", "args": {{ "type": "clear_alarms" }} }}

User: clear all timers
→ {{ "function": "clock", "args": {{ "type": "clear_timers" }} }}

User: get me information about my system
→ {{ "function": "system_control", "args": {{ "type": "get_system_info" }} }}

User: list running processes
→ {{ "function": "system_control", "args": {{ "type": "processes" }} }}

User: kill process with PID 1234
→ {{ "function": "system_control", "args": {{ "type": "kill_process", "process": 1234 }} }}

User: what is the system temperature?
→ {{ "function": "system_control", "args": {{ "type": "get_system_temperature" }} }}

User: shutdown the system
→ {{ "function": "system_control", "args": {{ "type": "immediate_action", "action": "shutdown" }} }}

User: restart the system
→ {{ "function": "system_control", "args": {{ "type": "immediate_action", "action": "restart" }} }}

User: logout the system
→ {{ "function": "system_control", "args": {{ "type": "immediate_action", "action": "logout" }} }}

User: sleep the system
→ {{ "function": "system_control", "args": {{ "type": "immediate_action", "action": "sleep" }} }}

User: hibernate the system
→ {{ "function": "system_control", "args": {{ "type": "immediate_action", "action": "hibernate" }} }}

User: what is the current volume?
→ {{ "function": "system_control", "args": {{ "type": "volume", "action": "get" }} }}

User: set volume to 50%
→ {{ "function": "system_control", "args": {{ "type": "volume", "action": "set", "value": 50 }} }}

User: increase volume by 10%
→ {{ "function": "system_control", "args": {{ "type": "volume", "action": "up", "value": 10 }} }}

User: decrease volume by 5%
→ {{ "function": "system_control", "args": {{ "type": "volume", "action": "down", "value": 5 }} }}

User: mute the volume
→ {{ "function": "system_control", "args": {{ "type": "volume", "action": "mute" }} }}

User: unmute the volume
→ {{ "function": "system_control", "args": {{ "type": "volume", "action": "unmute" }} }}

User: my name is Ayush
→ {{ "function": "fallback", "args": {{}} }}

Now respond to this user message:

ALWAYS reply in pure JSON.

User: """ + user_input

    try:
        raw_response = llm.invoke(prompt).strip()
        
        # Find JSON substring inside if the LLM adds fluff
        json_start = raw_response.find("{")
        json_end = raw_response.rfind("}") + 1
        json_block = raw_response[json_start:json_end]

        return json.loads(json_block)

    except Exception as e:
        print("[Intent parsing failed]", e)
        return {"function": "fallback", "args": {}, "error": str(e), "raw": raw_response}

# --- Prompt builder
def build_rag_prompt(user_input: str, memory_context_docs: list[str], about_context_docs: list[str]) -> str:
    memory_str = "\n".join(memory_context_docs)
    about_str = "\n".join(about_context_docs)
    return f"""
You are BitBud, a concise and intelligent personal AI agent.

Here are the last few things you talked about:
{memory_str}

Furthermore, here is some additional context about the user:
{about_str}

Instruction:
Given the user input below, respond in a short, factual, and helpful way using the above context **only if it's relevant**. Do **NOT** guess or overexplain. DO **NOT** use direct sentences from the contexts, make it sound more natural. If no context applies, respond naturally and ask clarification questions.

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


def text_to_shell_command(message: str) -> str:
    prompt = f"""You are a Linux command generator.
Given a user's request in plain English, output the most appropriate shell command.
Only output the shell command, nothing else. Do **NOT** include any explanations or additional text.

User: {message}
Command:"""
    cmd = llm.invoke(prompt).strip()
    return cmd if cmd else "echo 'No command generated'"




