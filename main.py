from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_transfer():
    data = request.get_json()
    parameters = data.get("queryResult", {}).get("parameters", {})
    
    amount = parameters.get("unit-currency", {}).get("amount", "N/A")
    currency = parameters.get("unit-currency", {}).get("currency", "USD")
    country = parameters.get("geo-country", "N/A")
    account = parameters.get("account_number", "N/A")
    bank = parameters.get("bank_name", "N/A")
    
    transfer_id = f"TXN{abs(hash(str(amount)+str(account))) % 100000:05d}"
    
    reply = (
        f"✅ Transfer initiated!\n"
        f"Amount: {currency} {amount}\n"
        f"To: {country} | Bank: {bank}\n"
        f"Account: {account}\n"
        f"Reference ID: {transfer_id}\n"
        f"ETA: 1-2 business days."
    )
    
    return jsonify({"fulfillmentText": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
