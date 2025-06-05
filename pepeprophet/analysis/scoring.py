def score_trend(market_data, sentiment_score):
    price = market_data['price']
    volume = market_data['volume']
    return (sentiment_score + (volume / 10000000)) / 2