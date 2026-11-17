from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/monitor/alive", methods=["GET"])
def alive():
    return jsonify({"status": "alive"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)