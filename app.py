from flask import Flask #for api
from flask import request #for query parameters
import os #for reading files

app = Flask(__name__)

LOG_DIR = "logs"
logs = []

def parse_logs():
    log_id = 1

    for file_name in os.listdir(LOG_DIR):
        file_path = os.path.join(LOG_DIR, file_name)

        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split("\t")

                if len(parts) != 4:
                    continue  

                log_entry = {
                    "id": log_id,
                    "timestamp": parts[0],
                    "level": parts[1],
                    "component": parts[2],
                    "message": parts[3]
                }

                logs.append(log_entry)
                log_id += 1

# Load logs when app starts
parse_logs()

@app.route("/logs", methods=["GET"])
def get_logs(): #filtering logs
    filtered_logs = logs

    level = request.args.get("level")
    component = request.args.get("component")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    if level:
        filtered_logs = [log for log in filtered_logs if log["level"] == level]

    if component:
        filtered_logs = [log for log in filtered_logs if log["component"] == component]

    if start_time:
        filtered_logs = [
            log for log in filtered_logs if log["timestamp"] >= start_time
        ]

    if end_time:
        filtered_logs = [
            log for log in filtered_logs if log["timestamp"] <= end_time
        ]

    return {
        "count": len(filtered_logs),
        "logs": filtered_logs
    }

@app.route("/logs/stats", methods=["GET"])
def get_log_stats(): #for health monitoring
    total_logs = len(logs)

    level_count = {}
    component_count = {}

    for log in logs:
        level = log["level"]
        component = log["component"]

        level_count[level] = level_count.get(level, 0) + 1
        component_count[component] = component_count.get(component, 0) + 1

    return {
        "total_logs": total_logs,
        "logs_per_level": level_count,
        "logs_per_component": component_count
    }

@app.route("/logs/<int:log_id>", methods=["GET"])
def get_log_by_id(log_id): #returns log details according to id else error handling
    for log in logs:
        if log["id"] == log_id:
            return log

    return {
        "error": "Log entry not found"
    }, 404

@app.route("/")
def home():
    return {"message": "Log API is running"}

if __name__ == "__main__":
    app.run(debug=True)

