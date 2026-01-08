from flask import Flask
import os

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

@app.route("/")
def home():
    return {"message": "Log API is running"}

if __name__ == "__main__":
    app.run(debug=True)