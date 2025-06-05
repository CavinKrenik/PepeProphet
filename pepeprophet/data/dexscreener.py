import requests

def fetch_dex_pair(address):
    url = f"https://api.dexscreener.com/latest/dex/pairs/ethereum/{address}"
    response = requests.get(url)
    data = response.json()

    if 'pair' not in data:
        raise ValueError("Invalid response from DexScreener")

    pair = data['pair']
    return {
        "price": float(pair["priceUsd"]),
        "volume": float(pair["volume"]["h24"]),
        "url": pair["url"]
    }
