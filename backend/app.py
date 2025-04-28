from flask import Flask, request, jsonify
from flask_cors import CORS
import psutil
import os
import json
import datetime
import requests
from cleanup import scan_files, delete_files  # Import cleanup functions
from tasks import get_process_data

app = Flask(__name__)
CORS(app)

# Together.ai API Configuration
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = "3f55913befac4ef77eb4e4e35e068d1adf8ca4306d90148e0e378e0733a9fb41"  # Hide in production!

headers = {
    "Authorization": f"Bearer {TOGETHER_API_KEY}",
    "Content-Type": "application/json"
}

# ------------------- SYSTEM HEALTH FUNCTIONS -------------------

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    return psutil.virtual_memory().percent

def get_disk_usage():
    return psutil.disk_usage('/').percent

def calculate_health_score(cpu, memory, disk):
    # Ensure each metric is within the 0-100 range
    cpu = max(0, min(cpu, 100))
    memory = max(0, min(memory, 100))
    disk = max(0, min(disk, 100))

    # Calculate the health score based on CPU, memory, and disk usage (no network usage)
    score = (100 - cpu) * 0.4 + (100 - memory) * 0.3 + (100 - disk) * 0.3
    
    # Ensure the score is within the range of 0 to 100
    score = max(0, min(score, 100))

    # To ensure a positive score, set a minimum threshold (e.g., score >= 10)
    score = max(score, 10)

    return round(score)


def save_daily_score(score):
    daily_scores_file = 'daily_scores.json'
    today = datetime.date.today().isoformat()

    if os.path.exists(daily_scores_file):
        with open(daily_scores_file, 'r') as f:
            daily_scores = json.load(f)
    else:
        daily_scores = {}

    daily_scores[today] = score

    with open(daily_scores_file, 'w') as f:
        json.dump(daily_scores, f, indent=4)

def get_health_data():
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    disk = get_disk_usage()

    # Calculate health score based on CPU, memory, and disk data
    health_score = calculate_health_score(cpu, memory, disk)
    
    # Save the health score to the daily scores file
    save_daily_score(health_score)

    return {
        'score': health_score,
        'cpuUsage': cpu,
        'memoryUsage': memory,
        'diskUsage': disk,
    }

# ------------------- ROUTES -------------------

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message')
    print(f"User Input: {user_input}")

    prompt = f"""
You are a technical assistant that helps diagnose and solve computer performance issues in detail.
Provide clear, actionable troubleshooting steps in 3 or more points.
Query: "{user_input}"
Answer:
"""

    try:
        response = requests.post(
            TOGETHER_API_URL,
            headers=headers,
            json={
                "model": "mistralai/Mistral-7B-Instruct-v0.1",
                "messages": [
                    {"role": "system", "content": "You are a helpful system diagnostics assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "top_p": 0.8,
                "max_tokens": 600
            }
        )

        if response.ok:
            bot_reply = response.json()["choices"][0]["message"]["content"]
            print(f"Bot Reply: {bot_reply}")
            return jsonify({"reply": bot_reply})
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return jsonify({"error": "Something went wrong with Together API!"}), 500

    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Junk File Scanning
@app.route('/api/scan', methods=['GET'])
def api_scan():
    files = scan_files()
    return jsonify({"status": "success", "files": files})

# Junk File Deletion
@app.route('/api/delete_junk', methods=['POST'])
def api_delete_junk():
    junk_files = scan_files()
    paths_to_delete = [file['path'] for file in junk_files]

    if not paths_to_delete:
        return jsonify({"status": "error", "message": "No junk files found to delete"}), 404

    deleted, errors = delete_files(paths_to_delete)

    if deleted:
        return jsonify({"status": "success", "message": f"Successfully deleted {len(deleted)} junk files", "deleted": deleted})
    elif errors:
        return jsonify({"status": "error", "message": "Error deleting files", "errors": errors}), 500
    else:
        return jsonify({"status": "error", "message": "Unknown error occurred"}), 500

# Selective File Deletion
@app.route('/api/delete', methods=['POST'])
def api_delete():
    data = request.get_json()
    paths = data.get('paths', [])

    if not paths:
        return jsonify({"status": "error", "message": "No files selected"}), 400

    deleted, errors = delete_files(paths)
    return jsonify({
        "status": "success",
        "deleted": deleted,
        "errors": errors
    })

# System Health Check
@app.route('/api/system_health', methods=['GET'])
def system_health():
    health_data = get_health_data()
    return jsonify(health_data)

@app.route('/processes', methods=['GET'])
def get_processes():
    processes = get_process_data()
    return jsonify(processes)

# ------------------- MAIN -------------------
if __name__ == '__main__':
    app.run(debug=True)
