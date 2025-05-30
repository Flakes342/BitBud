import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime

# Chroma client and embedding model
chroma_client = chromadb.PersistentClient(path="chromadb")

embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="/home/ayush/Documents/bitbud/models/paraphrase-MiniLM-L3-v2/"
)

collection = chroma_client.get_or_create_collection(
    name="bitbud-memory",
    embedding_function=embedding_func
)

# Remember a new memory
def remember(text: str, metadata: dict = None):
    print(collection.get()) 
    doc_id = str(hash(text))  # Simple hash for ID uniqueness
    try:
        print (f"[Memory] Saving memory: {text} with metadata: {metadata}")
        print ("Collection: ", collection)
        collection.add(
            documents=[text],
            metadatas=[metadata or {"note": "no metadata"}],
            ids=[doc_id]
        )
        print ("Collection after add: ", collection)
    except Exception as e:
        print(f"[Memory] Error saving memory: {e}")

# Recall similar memories
def recall(query: str, k: int = 3):
    print(f"[Recall] Querying for: {query}")
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    print(f"[Recall] Raw results: {results}")
    documents = results.get("documents", [])
    if documents:
        print(f"[Recall] Found: {documents[0]}")
        flattened = [doc for sublist in documents for doc in sublist]
        print(f"[Recall] Flattened: {flattened}")
        return list(set(flattened))

    print("[Recall] Nothing found.")
    return []


# Forget memory by matching the closest item to query
def forget(query: str):
    try:
        print ("Collection before delete: ", collection)
        print(f"[Memory] Forgetting memory matching: '{query}'")
        results = collection.query(
            query_texts=[query],
            n_results=1
        )
        ids = results.get("ids", [[]])[0]
        if ids:
            collection.delete(ids=ids)
            return f"Forgot memory matching: '{query}'"
        else:
            return f"No memory found matching: '{query}'"
    except Exception as e:
        print(f"[Memory] Forget error: {e}")
        return "Something went wrong while forgetting."
