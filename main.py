from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_transfer():
    data = request.get_json()
    
    # Get parameters from all contexts
    output_contexts = data.get("queryResult", {}).get("outputContexts", [])
    
    params = {}
    for context in output_contexts:
        params.update(context.get("parameters", {}))
    
    amount = params.get("unit-currency", {}).get("amount", "N/A")
    currency = params.get("unit-currency", {}).get("currency", "USD")
    country = params.get("geo-country", "N/A")
    account = params.get("account_number", "N/A")
    bank = params.get("bank_name", "N/A")
    
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
