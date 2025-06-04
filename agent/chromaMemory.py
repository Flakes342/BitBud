import requests
from chromadb import Client
from chromadb.config import Settings
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import uuid
from agent.llm import build_rag_prompt, generate_context_summary
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

embedding_func = HuggingFaceEmbeddings(
    model_name="/home/ayush/Documents/bitbud/models/paraphrase-MiniLM-L3-v2/"
)


vectorstore = Chroma(
    collection_name="bitbud",
    embedding_function=embedding_func,
    persist_directory="./bitbud_memory"
)

about_store = Chroma(
    collection_name="about_user",
    embedding_function=embedding_func,
    persist_directory="./chroma_about"
)

hist_about_text = ''
with open("ABOUT.md", "r") as f:
    about_text = f.read()
    if about_text.strip() != hist_about_text.strip():
        print("[Memory] About text was changed, updating memory...")
        hist_about_text = about_text
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_text(about_text)
        about_store.add_texts(chunks)



def store_to_memory(text: str, metadata: dict = None):
    context = generate_context_summary(text)
    metadata = metadata or {}
    metadata["context"] = context
    metadata["timestamp"] = datetime.now().isoformat()
    metadata["source"] = "conversation"

    vectorstore.add_texts(
        texts=[text],
        metadatas=[metadata]
    )

    print(f"[Memory] Stored: {text} with metadata: {metadata}")


def retrieve_context(query: str, k=5, score_threshold=0.75) -> list[str]:
    docs = vectorstore.similarity_search(query, k=k)
    
    query_context = generate_context_summary(query)
    if query_context:
        query_tokens = set(query_context.lower().split())

        filtered_docs = []
        for doc in docs:
            context_meta = doc.metadata.get("context", "").lower()
            if any(token in context_meta for token in query_tokens):
                filtered_docs.append(doc)
    else:
        filtered_docs = docs  # Fallback to embedding only

    results = [doc.page_content for doc in filtered_docs]
    print(f"[Memory] Retrieved (filtered): {results}")
    return results

def retrieve_about_context(query: str, k=3) -> list[str]:
    results = about_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]


#--------------------------------------------------------------------------------------------------------------------------------
# # Chroma client and embedding model
# chroma_client = chromadb.PersistentClient(path="chromadb")

# embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
#     model_name="/home/ayush/Documents/bitbud/models/paraphrase-MiniLM-L3-v2/"
# )

# collection = chroma_client.get_or_create_collection(
#     name="bitbud-memory",
#     embedding_function=embedding_func
# )


# # --- Store message to memory
# # def is_meaningful(text: str) -> bool:
# #     return len(text.split()) > 3 and not text.lower().strip() in {"ok", "sure", "yes", "no"}

# def store_to_memory(text: str, metadata: dict = None):
#     # if not is_meaningful(text):
#     #     return
#     metadata = metadata or {"source": "conversation"}
#     collection.add(
#         ids=[str(uuid.uuid4())],
#         documents=["User:"+text],
#         metadatas=[metadata]
#     )
#     print(f"[Memory] Stored: {text}")


# # --- Retrieve context given a query
# def retrieve_context(query: str, k=10, score_threshold=0.5, mmr=True) -> list[str]:
#     query_embedding = embedding_func([query])[0]
#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=k,
#         include=["documents", "distances"]
#     )

#     documents = results.get("documents", [[]])[0]
#     scores = results.get("distances", [[]])[0]

#     # Filter based on distance (lower is better)
#     filtered = list(set([doc for doc, dist in zip(documents, scores) if dist < (1 - score_threshold)]))
#     print(f"[Memory] Retrieved (filtered): {filtered}")
#     return filtered

#--------------------------------------------------------------------------------------------------------------------------------


# --- Prompt builder
def build_rag_prompt(user_input: str, context_docs: list[str]) -> str:
    context_str = "\n".join(context_docs)
    return f"""
You are BitBud, a concise and intelligent personal AI agent.

You have access to your following past conversations, memories and an about file provided by the user. 
{context_str}

Instruction:
Given the user input below, respond in a short, factual, and helpful way using the above context **only if it's relevant**. 
Do NOT guess or overexplain. Do NOT say random things. If no context applies, respond naturally but **briefly**.

User: "{user_input}"
""".strip()

# --- Main handler
def handle_user_input(user_input: str) -> str:
    store_to_memory(user_input)
    memory_context = retrieve_context(user_input)
    about_context = retrieve_about_context(user_input)

    context = memory_context + about_context

    prompt = build_rag_prompt(user_input, context)

    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3:4b",
        "prompt": prompt,
        "stream": False
    })

    reply = res.json().get("response", "...").strip()
    # store_to_memory(reply, metadata={"source": "assistant_reply"})
    return reply
