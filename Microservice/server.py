from flask import Flask, jsonify
from analyze_log import analyze_log

app = Flask(__name__)

metrics = analyze_log("log2.txt")

@app.get("/metrics")
def metrics_endpoint():
    return jsonify(metrics)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
