from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Remplace par tes vraies clés
master_key = "TON_MASTER_KEY"
private_key = "TON_PRIVATE_KEY"
public_key = "TON_PUBLIC_KEY"
token = "TON_TOKEN"

@app.route('/initier-paiement', methods=['GET'])
def initier_paiement():
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

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'PAYDUNYA-MASTER-KEY': master_key,
        'PAYDUNYA-PRIVATE-KEY': private_key,
        'PAYDUNYA-PUBLIC-KEY': public_key,
        'PAYDUNYA-TOKEN': token
    }

    response = requests.post(
        'https://app.paydunya.com/api/v1/checkout-invoice/create',
        json=data,
        headers=headers
    )

    res_data = response.json()

    if response.status_code == 200 and res_data.get('response_code') == '00':
        return redirect(res_data['response']['invoice_url'])
    else:
        return f"Erreur : {res_data.get('response_text', 'Impossible de générer le lien PayDunya')}", 400

if __name__ == '__main__':
    app.run()
