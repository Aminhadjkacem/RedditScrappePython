import praw
import os
from dotenv import load_dotenv

def connect_reddit():
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
    return reddit
'''
Scrapping from a specefic post
url="https://www.reddit.com/r/Sims4/comments/1ezzrxo/i_built_an_occult_emporium/"
post=reddit.submission(url=url)
'''
def get_positive_integer(prompt, allow_zero=False):
    """Helper function to get a positive integer input from the user."""
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            print("Exiting the program.")
            return None
        try:
            value = int(user_input)
            if value > 0 or (allow_zero and value == 0):
                return value
            else:
                print("Please enter a positive integer." if not allow_zero else "Please enter a non-negative integer.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
def choose_subreddit(reddit):
    # Choose a subreddit
    while True:
        subreddit_name = input("Enter the subreddit you want to scrape (or type 'exit' to quit): ").strip()
        
        if subreddit_name.lower() == 'exit':
            print("Exiting the program.")
            return None, None, None
        
        try:
            subreddit = reddit.subreddit(subreddit_name)
            # Test if the subreddit exists by trying to access its title
            _ = subreddit.title
            print(f"Subreddit '{subreddit_name}' found! Starting the scraping process...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Invalid subreddit or connection issue. Please try again.")
    
    # Get the number of posts and comments
    num_posts = get_positive_integer("Enter the number of posts to scrape: ")
    if num_posts is None: return None, None, None

    num_comments = get_positive_integer("Enter the number of comments to scrape per post: ", allow_zero=True)
    if num_comments is None: return None, None, None

    return subreddit, num_posts, num_comments


#subreddit = reddit.subreddit('fortnite') #choose the theme you want to scrap
def get_reddit_data(subreddit, num_posts, num_comment):
    for submission in subreddit.hot(limit=num_posts):
        print(f'Title: {submission.title}')
        print(f'Score: {submission.score}')
        print(f'URL: {submission.url}')
        print(f'Number of Comments: {submission.num_comments}')
        print(f'Content: {submission.selftext}')  # The main content of the post (for text posts)
        
        print('-' * 80)
        print('Top Comments:')
        
        # Fetch and print the top comments
        submission.comments.replace_more(limit=0)  # Avoid "More comments" sections
        top_comments = submission.comments.list()[:num_comment]  # Get the first `num_comments` comments
        
        for comment in top_comments:
            print(f'{comment.author}: {comment.body}')
            print('-' * 40)

        print('=' * 80)
# Fetch top 10 posts from the subreddit
reddit=connect_reddit()
if reddit:
    subreddit, num_posts, num_comments = choose_subreddit(reddit)
    get_reddit_data(subreddit,num_posts,num_comments)
else:
    print('Error: Could not connect to Reddit.')