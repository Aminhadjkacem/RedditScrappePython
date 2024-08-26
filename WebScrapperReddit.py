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
        if submission.num_comments<num_comment:
            num_comment=submission.num_comments
            print("-"*20,f"Number of comments requested is greater than the total number of comments. Fetching all {submission.num_comments} comments.","-"*20)
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

def scrape_reddit_post(url, num_comments):
    # Fetch the submission (post) using its URL
    post = reddit.submission(url=url)
    if num_comments>post.num_comments:
        num_comments=post.num_comments
        print("-"*20,f"Number of comments requested is greater than the total number of comments. Fetching all {num_comments} comments.","-"*20)
    # Print basic information about the post
    print(f'Title: {post.title}')
    print(f'Score: {post.score}')
    print(f'URL: {post.url}')
    print(f'Number of Comments: {post.num_comments}')
    print(f'Content: {post.selftext}')  # The main content of the post (for text posts)
    
    print('-' * 80)
    print('Top Comments:')
    
    # Fetch and print the top comments
    post.comments.replace_more(limit=0)  # Avoid "More comments" sections
    top_comments = post.comments.list()[:num_comments]  # Get the first `num_comments` comments
    
    for comment in top_comments:
        print(f'{comment.author}: {comment.body}')
        print('-' * 40)
    
    print('=' * 80)
def post_to_reddit(reddit):
    subreddit_name = input("Enter the subreddit you want to post to: ").strip()
    title = input("Enter the title of your post: ").strip()
    
    while True:
        post_type = input("Is this a (1) Text post or a (2) Link post? (type 'exit' to quit): ").strip()
        if post_type == '1':
            content = input("Enter the content of your text post: ").strip()
            try:
                subreddit = reddit.subreddit(subreddit_name)
                submission = subreddit.submit(title, selftext=content)
                print(f"Text post created successfully! Title: '{submission.title}'")
                print(f"URL: '{submission.url}'")
                return submission.url
            except Exception as e:
                print(f"An error occurred while creating the post: {e}")
            break
        elif post_type == '2':
            url = input("Enter the URL of your link post: ").strip()
            try:
                subreddit = reddit.subreddit(subreddit_name)
                submission = subreddit.submit(title, url=url)
                print(f"Link post created successfully! Title: '{submission.title}'")
                return submission
            except Exception as e:
                print(f"An error occurred while creating the post: {e}")
            break
        elif post_type.lower() == 'exit':
            print("Exiting the posting process.")
            return None
        else:
            print("Invalid input. Please enter '1' for a text post, '2' for a link post, or 'exit' to quit.")

# Fetch top 10 posts from the subreddit
def main_menu(reddit):
    if not reddit:
        print('Error: Could not connect to Reddit.')
        return

    while True:
        choice = input("Would you like to (1) Scrape from a Subreddit, (2) Scrape from a Specific Post, or (3) Post on Reddit? (type 'exit' to quit): ").strip()
        
        if choice.lower() == 'exit':
            print("Exiting the program.")
            break
        
        if choice == '1':
            subreddit, num_posts, num_comments = choose_subreddit(reddit)
            if subreddit:
                get_reddit_data(subreddit, num_posts, num_comments)
            else:
                print("Scraping cancelled or no subreddit chosen.")
        
        elif choice == '2':
            url = input("Enter the Reddit post URL: ").strip()
            try:
                num_comments = int(input("Enter the number of comments to scrape: ").strip())
                if num_comments >= 0:
                    scrape_reddit_post(url, num_comments)
                else:
                    print("Please enter a non-negative integer for the number of comments.")
            except ValueError:
                print("Invalid input. Please enter a valid number for comments.")
        
        elif choice == '3':
            url=post_to_reddit(reddit)
        
        else:
            print("Invalid choice. Please enter '1' to scrape a subreddit, '2' to scrape")
# Call the main menu function
reddit=connect_reddit()
if reddit:
    main_menu(reddit)
else:
    print("Error: Could not connect to Reddit.Please check your credentials in the .env file.")