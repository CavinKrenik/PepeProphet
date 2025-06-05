from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_sentiment(posts):
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(post)['compound'] for post in posts]
    return sum(scores) / len(scores) if scores else 0