import requests
from chromadb import Client
from chromadb.config import Settings
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import uuid


# Chroma client and embedding model
chroma_client = chromadb.PersistentClient(path="chromadb")

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="/home/ayush/Documents/bitbud/models/paraphrase-MiniLM-L3-v2/"
)

collection = chroma_client.get_or_create_collection(
    name="bitbud-memory",
    embedding_function=embedding_func
)


# --- Store message to memory
# def is_meaningful(text: str) -> bool:
#     return len(text.split()) > 3 and not text.lower().strip() in {"ok", "sure", "yes", "no"}

def store_to_memory(text: str, metadata: dict = None):
    # if not is_meaningful(text):
    #     return
    metadata = metadata or {"source": "conversation"}
    collection.add(
        ids=[str(uuid.uuid4())],
        documents=[text],
        metadatas=[metadata]
    )
    print(f"[Memory] Stored: {text}")


# --- Retrieve context given a query
def retrieve_context(query: str, k=10, score_threshold=0.5, mmr=True) -> list[str]:
    query_embedding = embedding_func([query])[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "distances"]
    )

    documents = results.get("documents", [[]])[0]
    scores = results.get("distances", [[]])[0]

    # Filter based on distance (lower is better)
    filtered = list(set([doc for doc, dist in zip(documents, scores) if dist < (1 - score_threshold)]))
    print(f"[Memory] Retrieved (filtered): {filtered}")
    return filtered


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

# --- Main handler
def handle_user_input(user_input: str) -> str:
    store_to_memory(user_input)
    context = retrieve_context(user_input)
    prompt = build_rag_prompt(user_input, context)

    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:4b",
        "prompt": prompt,
        "stream": False
    })

    reply = res.json().get("response", "...").strip()
    store_to_memory(reply, metadata={"source": "assistant_reply"})
    return reply
