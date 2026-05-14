from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database
accounts = {}
next_id = 1


@app.route("/accounts", methods=["POST"])
def create_account():
    """Create a new account"""
    global next_id

    data = request.get_json()
    account = {
        "id": next_id,
        "name": data.get("name"),
        "email": data.get("email"),
        "address": data.get("address"),
    }

    accounts[next_id] = account
    next_id += 1

    return jsonify(account), 201


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all accounts"""
    return jsonify(list(accounts.values())), 200


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """Get a single account"""
    account = accounts.get(account_id)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    return jsonify(account), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an account"""
    account = accounts.get(account_id)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    data = request.get_json()

    account["name"] = data.get("name", account["name"])
    account["email"] = data.get("email", account["email"])
    account["address"] = data.get("address", account["address"])

    return jsonify(account), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an account"""
    if account_id not in accounts:
        return jsonify({"error": "Account not found"}), 404

    del accounts[account_id]

    return jsonify({"message": "Account deleted successfully"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
