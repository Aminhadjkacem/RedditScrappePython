import praw
import os
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = os.getenv('REDDIT_USER_AGENT')
username = os.getenv('REDDIT_USERNAME')
password = os.getenv('REDDIT_PASSWORD')

# Create Reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)
'''
Scrapping from a specefic post
url="https://www.reddit.com/r/Sims4/comments/1ezzrxo/i_built_an_occult_emporium/"
post=reddit.submission(url=url)
'''
# Choose a subreddit
subreddit = reddit.subreddit('fortnite') #choose the theme you want to scrap

# Fetch top 10 posts from the subreddit
for submission in subreddit.hot(limit=10):
    print(f'Title: {submission.title}')
    print(f'Score: {submission.score}')
    print(f'URL: {submission.url}')
    print(f'Number of Comments: {submission.num_comments}')
    print(f'Content: {submission.selftext}')  # The main content of the post (text post)
    
    print('-' * 80)
    print('Top Comments:')
    
    # Fetch and print the top comments
    submission.comments.replace_more(limit=0)  # Avoid "More comments" sections
    for comment in submission.comments.list()[:5]:  # Get the first 5 comments
        print("comment of",f'{comment.author}: {comment.body}')
        print('-' * 40)

    print('=' * 80)