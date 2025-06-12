# api/convert.py
import json
import requests

def handler(request, context):
    api_key = '34d4a034f93d04d39558'
    url = f"https://free.currconv.com/api/v7/convert?q=EUR_USD&compact=ultra&apiKey={api_key}"
    
    try:
        amount = float(request.get("queryStringParameters", {}).get("amount", 0))
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data.get("EUR_USD", None)
        if rate is not None:
            converted = amount * rate
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"eur": amount, "usd": round(converted, 2), "rate": rate})
            }
        else:
            raise ValueError("No rate found")
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }
