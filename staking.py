
from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder='explorer_frontend')

wallets = {"test-wallet": {"nun_tokens": 51000000, "staked": 25000000, "rewards": 4200}}

@app.route('/balance/<wallet>')
def balance(wallet):
    return jsonify({**wallets.get(wallet, {}), "wallet": wallet})

@app.route('/stake', methods=['POST'])
def stake():
    data = request.get_json()
    w = wallets[data['wallet']]
    amount = data['amount']
    if w['nun_tokens'] >= amount:
        w['nun_tokens'] -= amount
        w['staked'] += amount
        w['rewards'] += amount * 0.01
    return jsonify(w)

@app.route('/unstake', methods=['POST'])
def unstake():
    data = request.get_json()
    w = wallets[data['wallet']]
    w['nun_tokens'] += w['staked']
    w['staked'] = 0
    return jsonify(w)

@app.route('/claim', methods=['POST'])
def claim():
    data = request.get_json()
    w = wallets[data['wallet']]
    w['nun_tokens'] += w['rewards']
    w['rewards'] = 0
    return jsonify(w)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'explorer.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(port=5000)
