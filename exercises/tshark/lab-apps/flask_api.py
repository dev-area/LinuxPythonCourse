#!/usr/bin/env python3
"""Minimal Flask REST API. Run on the QEMU guest (192.168.0.2).
    pip install flask
    python3 flask_api.py
Endpoints:
    GET  /api/items          -> list items
    GET  /api/items/<id>     -> one item (404 if missing)
    POST /api/items          -> create item  (JSON body: {"name": "..."})
    GET  /api/boom           -> raises 500 (for the troubleshooting stage)
"""
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
ITEMS = {1: "alpha", 2: "beta"}


@app.get("/api/items")
def list_items():
    return jsonify(ITEMS)


@app.get("/api/items/<int:item_id>")
def get_item(item_id):
    if item_id not in ITEMS:
        abort(404)
    return jsonify({item_id: ITEMS[item_id]})


@app.post("/api/items")
def create_item():
    data = request.get_json(silent=True) or {}
    if "name" not in data:
        abort(400, description="missing 'name'")
    new_id = max(ITEMS) + 1
    ITEMS[new_id] = data["name"]
    return jsonify({new_id: data["name"]}), 201


@app.get("/api/boom")
def boom():
    raise RuntimeError("intentional 500 for the lab")


if __name__ == "__main__":
    # host=0.0.0.0 so the DEBIAN host can reach it over 192.168.0.2
    app.run(host="0.0.0.0", port=5000)
