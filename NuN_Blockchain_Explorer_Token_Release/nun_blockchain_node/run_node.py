# run_node.py – Node runtime with explorer and transaction/mine support

from flask import Flask, request, jsonify
import time

app = Flask(__name__)
blockchain = [{
    "index": 0,
    "data": "Genesis Block",
    "timestamp": time.time()
}]
mempool = []

@app.route('/status')
def status():
    return jsonify({
        "node": "NuN Blockchain Node",
        "status": "online",
        "chain_length": len(blockchain),
        "peers": 0,
        "latest_block": blockchain[-1]
    })

@app.route('/tx/new', methods=['POST'])
def new_tx():
    data = request.json
    mempool.append(data)
    return jsonify({"message": "Transaction received", "tx": data})

@app.route('/mine', methods=['POST'])
def mine_block():
    block = {
        "index": len(blockchain),
        "data": mempool.copy(),
        "timestamp": time.time()
    }
    blockchain.append(block)
    mempool.clear()
    return jsonify({"message": "Block mined", "block": block})

@app.route('/explorer')
def explorer():
    return jsonify({
        "blocks": blockchain,
        "mempool": mempool
    })

if __name__ == '__main__':
    print("🔗 NuN Blockchain Node running at http://127.0.0.1:5000")
    app.run(port=5000)
