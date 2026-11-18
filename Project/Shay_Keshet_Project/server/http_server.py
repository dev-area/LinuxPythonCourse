
from flask import Flask, jsonify, request
from datetime import datetime, timezone
import os
import time

app = Flask(__name__)


# 1. Check if the server is alive
@app.route("/alive", methods=["GET"])
def alive():
    return jsonify({"status": "alive"})


# 2. Read temperature
@app.route("/temperature", methods=["GET"])
def temperature():
    # Simulated temperature: 25.5 degrees Celsius
    return jsonify({"celsius": 25.5})


# 3. Read the system clock
@app.route("/rtc", methods=["GET"])
def rtc():
    now = datetime.now(timezone.utc)

    return jsonify({
        "unix": int(now.timestamp()),
        "iso": now.isoformat()
    })


# 4. Read free memory
@app.route("/memory", methods=["GET"])
def memory():
    free_kb = 0

    with open("/proc/meminfo", "r") as file:
        for line in file:
            if line.startswith("MemAvailable:"):
                free_kb = int(line.split()[1])
                break

    return jsonify({"free_kb": free_kb})


# 5. Read CPU usage
def read_cpu_times():
    with open("/proc/stat", "r") as file:
        values = file.readline().split()

    times = list(map(int, values[1:]))
    idle = times[3] + times[4]
    total = sum(times)

    return idle, total


@app.route("/cpu", methods=["GET"])
def cpu():
    idle1, total1 = read_cpu_times()
    time.sleep(0.2)
    idle2, total2 = read_cpu_times()

    total_diff = total2 - total1
    idle_diff = idle2 - idle1

    usage = 0.0

    if total_diff > 0:
        usage = 100 * (1 - idle_diff / total_diff)

    return jsonify({
        "usage_percent": round(usage, 1)
    })


# 6. Read free storage
@app.route("/storage", methods=["GET"])
def storage():
    stats = os.statvfs("/")

    free_bytes = stats.f_bavail * stats.f_frsize

    return jsonify({"free_bytes": free_bytes})


# 7. Read alerts
alerts = []


@app.route("/alerts", methods=["GET"])
def get_alerts():
    try:
        since = int(request.args.get("since", 0))
    except ValueError:
        return jsonify({"error": "Invalid since value"}), 400

    new_alerts = [
        alert for alert in alerts
        if alert["id"] > since
    ]

    return jsonify({"alerts": new_alerts})


if __name__ == "__main__":
    print("HTTP Monitor Server is starting...")

    app.run(
        host="0.0.0.0",
        port=5001
    )
