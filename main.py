from flask import Flask, request, jsonify
from agent.langGraphRouter import build_graph

app = Flask(__name__)
# CORS(app)
graph = build_graph()

@app.route("/")
def home():
    return "BitBud backend is running!"

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    result = graph.invoke({"input": user_input})
    return jsonify({"reply": result.get("output", "I got nothing!")})

if __name__ == "__main__":
    app.run(port=5001)

