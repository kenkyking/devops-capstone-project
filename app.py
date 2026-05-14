"""
Application routes
"""

from flask import Flask, jsonify, request
from service.models import Account, init_db
from service import config

######################################################################
# Create Flask app
######################################################################

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    config.SQLALCHEMY_DATABASE_URI
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
    config.SQLALCHEMY_TRACK_MODIFICATIONS
)

app.config["SECRET_KEY"] = config.SECRET_KEY

######################################################################
# Initialize Database
######################################################################

init_db(app)

######################################################################
# ROUTES
######################################################################


@app.route("/accounts", methods=["POST"])
def create_account():
    """Create an Account"""

    data = request.get_json()

    account = Account()
    account.deserialize(data)
    account.create()

    return jsonify(account.serialize()), 201


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts"""

    accounts = Account.all()
    results = [account.serialize() for account in accounts]

    return jsonify(results), 200


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    """Get an Account by ID"""

    account = Account.find(account_id)

    if not account:
        return jsonify({"message": "Account not found"}), 404

    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an existing Account"""

    account = Account.find(account_id)

    if not account:
        return jsonify({"message": "Account not found"}), 404

    data = request.get_json()

    account.deserialize(data)
    account.id = account_id
    account.update()

    return jsonify(account.serialize()), 200


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an Account"""

    account = Account.find(account_id)

    if not account:
        return jsonify({"message": "Account not found"}), 404

    account.delete()

    return "", 204


######################################################################
# MAIN PROGRAM
######################################################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
