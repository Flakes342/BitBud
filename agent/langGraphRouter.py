from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from agent.tools.app_launcher import open_app
from agent.tools.recommend import recommend_music
from agent.tools.search import search_web
from agent.llm import get_intent, summarize_memories
from agent.chromaMemory import remember, forget, recall

# State
class BitBudState(TypedDict,total=False):
    input: str
    output: str
    function: str
    args: dict


import urllib.parse

def parse_args(args):
    if isinstance(args, dict):
        return args
    if isinstance(args, str):
        return dict(urllib.parse.parse_qsl(args))
    return {}

def route_input(state):
    user_input = state["input"]
    result = get_intent(user_input)
    # print("Intent result:", result)

    func = result.get("function")
    args = parse_args(result.get("args", {}))

    print(f"Routing function: {func} with args: {args}")

    if func == "remember":
        text = args.get("text", "")
        if not text.strip():
            return {"function": "remember", "args": {"text": text}, "output": "I need something to remember."}
        remember(text)
        return {"function": "remember", "args": {"text": text}, "output": f"Got it. I’ll remember: '{text}'"}

    elif func == "forget":
        text = args.get("text", "")
        msg = forget(text)
        return {"function": "forget", "args": {"text": text}, "output": msg}

    elif func == "recall":
        query = args.get("text", "")  # FIXED this line
        results = recall(query)
        return {
            "function": "recall",
            "args": {"text": query},
            "output": summarize_memories(results, query) if results else "I don’t remember anything like that."
        }

    elif func in ["open_app", "recommend_music", "search_web"]:
        return {"function": func, "args": args}

    return {"function": "fallback", "args": {}, "output": "Sorry, I didn’t understand that."}


# Custom functions to handle each intent
def handle_open_app(state): 
    print(f"Opening app: {state['args'].get('name', '')}")
    return {"output": open_app(state["args"].get("name", ""))}
def handle_recommend_music(state): 
    return {"output": recommend_music()}
def handle_search_web(state): 
    return {"output": search_web(state["args"].get("query", ""))}
def remember_handler(state): 
    return {"output": remember(state["args"].get("text", ""))}
def forget_handler(state): 
    return {"output": forget(state["args"].get("text", ""))}
def recall_handler(state): 
    return {"output": recall(state["args"].get("text", ""))}
def fallback(state): 
    return {"output": "Sorry, I didn’t understand that."}

# LangGraph router setup
def build_graph():
    graph = StateGraph(BitBudState)
    # print(graph)

    graph.add_node("route_input", RunnableLambda(route_input))
    graph.add_node("open_app", RunnableLambda(handle_open_app))
    graph.add_node("recommend_music", RunnableLambda(handle_recommend_music))
    graph.add_node("search_web", RunnableLambda(handle_search_web))
    graph.add_node("remember", RunnableLambda(remember_handler))
    graph.add_node("forget", RunnableLambda(forget_handler))
    graph.add_node("recall", RunnableLambda(recall_handler))

    graph.add_node("fallback", RunnableLambda(fallback))

    # Define routing logic
    def decide_next_node(state):
        func = state.get("function")
        if func == "open_app": 
            return "open_app"
        elif func == "recommend_music": 
            return "recommend_music"
        elif func == "search_web": 
            return "search_web"
        elif func == "remember": 
            return "remember"
        elif func == "forget":
            return "forget"
        elif func == "recall":
            return "recall"
        return "fallback"

    graph.set_entry_point("route_input")
    graph.add_conditional_edges("route_input", decide_next_node)
    graph.add_edge("open_app", END)
    graph.add_edge("recommend_music", END)
    graph.add_edge("search_web", END)
    graph.add_edge("remember", END)
    graph.add_edge("forget", END)
    graph.add_edge("recall", END)
    graph.add_edge("fallback", END)

    return graph.compile()
