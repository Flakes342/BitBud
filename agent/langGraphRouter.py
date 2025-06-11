import urllib.parse
from typing import TypedDict
from agent.llm import get_intent
from agent.tools.clock import clock
from agent.tools.search import search_web
from langgraph.graph import StateGraph, END
from agent.tools.app_launcher import open_app
from agent.chromaMemory import handle_user_input 
from agent.tools.recommend import recommend_music
from langchain_core.runnables import RunnableLambda
from agent.tools.shell_command import linux_commands


# --- BitBud state
class BitBudState(TypedDict, total=False):
    input: str
    output: str
    function: str
    args: dict

def parse_args(args):
    if isinstance(args, dict):
        return args
    if isinstance(args, str):
        return dict(urllib.parse.parse_qsl(args))
    return {}

# --- Route input to functions or fallback to RAG
def route_input(state):
    user_input = state["input"]
    result = get_intent(user_input)

    func = result.get("function")
    args = parse_args(result.get("args", {}))
    print(f"[Router] Function: {func}, Args: {args}")

    if func == "open_app":
        return {"function": "open_app", "args": args}
    elif func == "recommend_music":
        return {"function": "recommend_music", "args": args}
    elif func == "search_web":
        return {"function": "search_web", "args": args}
    elif func == "linux_commands":
        return {"function": "linux_commands", "args": args}
    elif func == "clock":
        return {"function": "clock", "args": args}

    # For anything else (remember, recall, fallback): RAG
    rag_response = handle_user_input(user_input)
    return {
        "function": "fallback",
        "args": {},
        "output": rag_response
    }

# --- Intent handlers
def handle_open_app(state): 
    name = state["args"].get("name", "")
    query = state["args"].get("query", "")
    return {"output": open_app(name, query)} #changed to match new open_app signature

def handle_recommend_music(state): 
    return {"output": recommend_music()}

def handle_search_web(state): 
    return {"output": search_web(state["args"].get("query", ""))}

def handle_linux_commands(state): 
    return {"output": linux_commands(state["args"].get("command", ""))}

def handle_clock(state):
    args = state["args"]
    return {"output": clock(args)}

def fallback_handler(state): 
    return {"output": state.get("output", "Hmm, not sure what you meant.")}

# --- Build LangGraph
def build_graph():
    graph = StateGraph(BitBudState)

    graph.add_node("route_input", RunnableLambda(route_input))
    graph.add_node("open_app", RunnableLambda(handle_open_app))
    graph.add_node("recommend_music", RunnableLambda(handle_recommend_music))
    graph.add_node("search_web", RunnableLambda(handle_search_web))
    graph.add_node("linux_commands", RunnableLambda(handle_linux_commands))
    graph.add_node("clock", RunnableLambda(handle_clock))

    graph.add_node("fallback", RunnableLambda(fallback_handler))

    def decide_next_node(state):
        func = state.get("function")
        if func == "open_app": return "open_app"
        if func == "recommend_music": return "recommend_music"
        if func == "search_web": return "search_web"
        if func == "linux_commands": return "linux_commands"
        if func == "clock": return "clock"
        return "fallback"

    graph.set_entry_point("route_input")
    graph.add_conditional_edges("route_input", decide_next_node)

    graph.add_edge("open_app", END)
    graph.add_edge("recommend_music", END)
    graph.add_edge("search_web", END)
    graph.add_edge("linux_commands", END)
    graph.add_edge("clock", END)
    graph.add_edge("fallback", END)

    return graph.compile()
