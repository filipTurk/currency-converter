# api/convert.py
import json
import requests
import os

def handler(request, context):
    API_KEY = os.getenv("API_KEY")
    url = f"https://api.currencyapi.com/v3/latest?apikey={API_KEY}&currencies=EUR,USD"
    if not API_KEY:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "API_KEY environment variable is not set."})
        }
    try:
        amount_str = request.get("queryStringParameters", {}).get("amount", "0")
        amount = float(amount_str)

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        eur_value = data["data"]["EUR"]["value"]
        usd_value = data["data"]["USD"]["value"]

        eur_to_usd = usd_value / eur_value

        converted = amount * eur_to_usd
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "eur": amount,
                "usd": round(converted, 2),
                "rate": round(eur_to_usd, 4)
            })
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
