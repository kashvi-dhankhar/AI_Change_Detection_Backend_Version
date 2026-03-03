from flask import Flask, render_template, request, jsonify, Response
import os
import tempfile

from pipeline.task_manager import (
    start_task,
    get_status_stream,
    get_result
)

app = Flask(__name__)


# --------------------------------------------------
# HOME
# --------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------
# START DETECTION
# --------------------------------------------------
@app.route("/start", methods=["POST"])
def start_detection():
    if "kml" not in request.files:
        return jsonify({"error": "KML file missing"}), 400

    kml_file = request.files["kml"]
    from_date = request.form.get("from_date")
    to_date = request.form.get("to_date")

    if not from_date or not to_date:
        return jsonify({"error": "Dates missing"}), 400

    # Save KML temporarily
    tmp_dir = tempfile.mkdtemp()
    kml_path = os.path.join(tmp_dir, kml_file.filename)
    kml_file.save(kml_path)

    try:
        start_task(kml_path, from_date, to_date)
        return jsonify({"status": "Started"}), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 409


# --------------------------------------------------
# STATUS STREAM (SSE)
# --------------------------------------------------
@app.route("/status-stream")
def status_stream():
    return Response(
        get_status_stream(),
        mimetype="text/event-stream"
    )


# --------------------------------------------------
# RESULT
# --------------------------------------------------
@app.route("/result")
def result():
    data = get_result()
    return jsonify(data if data else {})


# --------------------------------------------------
# RUN
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
