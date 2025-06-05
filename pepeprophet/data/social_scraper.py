import os
import praw

def fetch_reddit_posts():
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    subreddit = reddit.subreddit("CryptoCurrency+PepeCoin+memecoins")
    posts = []
    
    for post in subreddit.new(limit=10):
        if "pepe" in post.title.lower():
            posts.append(post.title)

    return posts
