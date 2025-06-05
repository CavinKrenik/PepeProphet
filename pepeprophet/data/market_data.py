import requests

def fetch_market_data(coin_ids=["ripple", "peanut", "shiba-inu"]):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(coin_ids)
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        results = {}
        for coin in data:
            results[coin["id"]] = {
                "price": coin["current_price"],
                "volume": coin["total_volume"]
            }

        return results

    except Exception as e:
        print(f"[MarketData] Error: {e}")
        return {}
