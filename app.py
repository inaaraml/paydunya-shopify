import os
from flask import Flask, request, redirect, jsonify
import requests

app = Flask(__name__)

# Remplace par tes vraies clés ou mieux, utilise des variables d'environnement
master_key = os.getenv("PAYDUNYA_MASTER_KEY", "TON_MASTER_KEY")
private_key = os.getenv("PAYDUNYA_PRIVATE_KEY", "TON_PRIVATE_KEY")
public_key = os.getenv("PAYDUNYA_PUBLIC_KEY", "TON_PUBLIC_KEY")
token = os.getenv("PAYDUNYA_TOKEN", "TON_TOKEN")

@app.route('/initier-paiement', methods=['POST'])
def initier_paiement():
    # Define the data to be sent to PayDunya
    data = {
        "invoice": {
            "items": [
                {
                    "name": "Commande Shopify",
                    "quantity": 1,
                    "unit_price": 1000,
                    "total_price": 1000,
                    "description": "Paiement via Shopify"
                }
            ],
            "total_amount": 1000,
            "description": "Commande Shopify"
        },
        "store": {
            "name": "Ma boutique",
            "website_url": "https://ton-site-shopify.com"
        },
        "actions": {
            "callback_url": "https://tonserveur.com/callback",
            "return_url": "https://ton-site-shopify.com/merci"
        }
    }

    # Headers for the PayDunya API request
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'PAYDUNYA-MASTER-KEY': master_key,
        'PAYDUNYA-PRIVATE-KEY': private_key,
        'PAYDUNYA-PUBLIC-KEY': public_key,
        'PAYDUNYA-TOKEN': token
    }

    # Call the PayDunya API to initiate the payment
    try:
        response = requests.post(
            'https://app.paydunya.com/api/v1/checkout-invoice/create',
            json=data,
            headers=headers
        )

        # Get the response data
        res_data = response.json()

        if response.status_code == 200 and res_data.get('response_code') == '00':
            # If the payment initiation is successful, redirect to the PayDunya checkout page
            return redirect(res_data['response']['invoice_url'])
        else:
            # If there's an error, return a message with the error
            return jsonify({
                "message": f"Erreur : {res_data.get('response_text', 'Impossible de générer le lien PayDunya')}"
            }), 400

    except requests.exceptions.RequestException as e:
        # If there’s an error with the request, return an error message
        return jsonify({
            "message": f"Erreur de communication avec PayDunya: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Run the app on all available interfaces and on port 10000
    app.run(host='0.0.0.0', port=10000)
