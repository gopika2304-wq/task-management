from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime
import requests

app = Flask(__name__)

tasks = []  # Store tasks in-memory for simplicity
GROQ_API_KEY = "your_groq_api_key"  # Replace with your actual API key
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

def get_ai_suggestion(task_list):
    """Get AI-generated task prioritization suggestions."""
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    prompt = f"Prioritize the following tasks based on urgency and importance:\n{task_list}"
    data = {
        "model": "llama3-8b",
        "messages": [{"role": "system", "content": "You are a helpful assistant."},
                     {"role": "user", "content": prompt}]
    }
    response = requests.post(GROQ_API_URL, json=data, headers=headers)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No suggestion")

@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task_desc = request.form["task"]
    deadline = request.form["deadline"]
    tasks.append({"task": task_desc, "deadline": deadline})
    return redirect(url_for("index"))

@app.route("/get_suggestions", methods=["GET"])
def get_suggestions():
    task_list = "\n".join([f"{t['task']} (Deadline: {t['deadline']})" for t in tasks])
    suggestion = get_ai_suggestion(task_list)
    return jsonify({"suggestion": suggestion})

if __name__ == "__main__":
    app.run(debug=True)
          