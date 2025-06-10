from flask import Flask, request, jsonify
from agent.langGraphRouter import build_graph
import logging
from logging.handlers import RotatingFileHandler

# Logging Setup

log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
log_handler = RotatingFileHandler('bitbud.log', maxBytes=1000000, backupCount=3)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

# Flask App Setup

app = Flask(__name__)
graph = build_graph() # Initialize the LangGraph

@app.route("/")
def home():
    return "BitBud backend is running!"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(force=True)
        if not data or "message" not in data:
            logger.warning("Bad request: missing 'message'")
            return jsonify({"error": "Missing 'message' field"}), 400

        user_input = data["message"]
        logger.info(f"User input received: {user_input}")

        result = graph.invoke({"input": user_input})
        reply = result.get("output", "I got nothing!")

        logger.debug(f"Reply generated: {reply}")
        return jsonify({"reply": reply})

    except Exception as e:
        logger.exception("Exception in /ask endpoint")
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting BitBud backend on port 5001")
    app.run(port=5001)
