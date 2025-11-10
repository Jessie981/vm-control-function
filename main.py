from flask import Flask, request, jsonify
from googleapiclient import discovery
from google.auth import default
import os

app = Flask(__name__)

@app.route("/", methods=["POST"])
def control_vm():
    try:
        request_json = request.get_json(force=True)
        action = request_json.get("action")
        project = request_json.get("project_id")
        zone = request_json.get("zone")
        instance = request_json.get("instance_name")

        credentials, _ = default()
        service = discovery.build("compute", "v1", credentials=credentials)

        if action == "start":
            result = service.instances().start(project=project, zone=zone, instance=instance).execute()
        elif action == "stop":
            result = service.instances().stop(project=project, zone=zone, instance=instance).execute()
        else:
            return jsonify({"error": "Invalid action"}), 400

        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)