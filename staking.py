"""NuN staking API sandbox. In-memory demo only; not production-safe."""
from copy import deepcopy
import math
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="explorer_frontend")
_INITIAL = {"test-wallet": {"nun_tokens": 51000000, "staked": 25000000, "rewards": 4200.0}}
wallets = deepcopy(_INITIAL)

def body():
    value = request.get_json(silent=True)
    return value if isinstance(value, dict) else None

def get_wallet(data):
    name = data.get("wallet") if data else None
    if not isinstance(name, str) or not name:
        return None, (jsonify({"error": "wallet must be a non-empty string"}), 400)
    record = wallets.get(name)
    if record is None:
        return None, (jsonify({"error": "wallet not found"}), 404)
    return record, None

def valid_amount(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0

@app.get("/health")
def health():
    return jsonify({"status": "ok", "mode": "sandbox-only", "storage": "in-memory"}), 200

@app.get("/balance/<wallet>")
def balance(wallet):
    record = wallets.get(wallet)
    if record is None:
        return jsonify({"error": "wallet not found"}), 404
    return jsonify({**record, "wallet": wallet}), 200

@app.post("/stake")
def stake():
    data = body()
    if data is None:
        return jsonify({"error": "request body must be a JSON object"}), 400
    record, error = get_wallet(data)
    if error:
        return error
    amount = data.get("amount")
    if not valid_amount(amount):
        return jsonify({"error": "amount must be a finite positive number"}), 400
    if amount > record["nun_tokens"]:
        return jsonify({"error": "insufficient balance"}), 400
    record["nun_tokens"] -= amount
    record["staked"] += amount
    record["rewards"] += amount * 0.01
    return jsonify(record), 200

@app.post("/unstake")
def unstake():
    data = body()
    if data is None:
        return jsonify({"error": "request body must be a JSON object"}), 400
    record, error = get_wallet(data)
    if error:
        return error
    amount = data.get("amount", record["staked"])
    if not valid_amount(amount):
        return jsonify({"error": "amount must be a finite positive number"}), 400
    if amount > record["staked"]:
        return jsonify({"error": "insufficient staked balance"}), 400
    record["staked"] -= amount
    record["nun_tokens"] += amount
    return jsonify(record), 200

@app.post("/claim")
def claim():
    data = body()
    if data is None:
        return jsonify({"error": "request body must be a JSON object"}), 400
    record, error = get_wallet(data)
    if error:
        return error
    amount = record["rewards"]
    record["nun_tokens"] += amount
    record["rewards"] = 0.0
    return jsonify({**record, "claimed": amount}), 200

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "explorer.html")

@app.route("/<path:path>")
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
