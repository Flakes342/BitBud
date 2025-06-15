import re
from langchain_community.llms import Ollama
from typing import Optional, TypedDict
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

llm = Ollama(model="gemma3:4b")

def load_system_prompt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()

SYSTEM_PROMPT_PATH = "agent/prompts/system_prompt.txt"
system_prompt = load_system_prompt(SYSTEM_PROMPT_PATH)


prompt = PromptTemplate.from_template(system_prompt)

def get_intent(user_input):
    prompt = system_prompt + user_input

    try:
        raw_response = llm.invoke(prompt).strip()
        print (raw_response, "Raw RESPONSE")

        # json_start = raw_response.find("{")
        # json_end = raw_response.rfind("}") + 1
        # json_block = raw_response[json_start:json_end]

        json_block = re.sub(r"^```(?:json)?\n|\n```$", "", raw_response.strip(), flags=re.IGNORECASE) # Removing md block ''' ''' 

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




