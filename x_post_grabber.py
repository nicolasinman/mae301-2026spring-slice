# Script to fetch tweets for usernames in x_handles.txt using twint
# and save all tweet texts as plain text to a .txt file.

import twint
import os

def read_usernames(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def fetch_tweets(username, since_date):
    """Fetch tweets for a user since a given date."""
    tweets = []
    temp_file = f"temp_{username}.txt"
    
    try:
        c = twint.Config()
        c.Username = username
        c.Since = since_date
        c.Output = temp_file
        c.Store_csv = False
        
        # Run the search and save to temp file
        twint.run.Search(c)
        
        # Read tweets from temp file
        if os.path.exists(temp_file):
            with open(temp_file, 'r', encoding='utf-8', errors='ignore') as f:
                tweets = [line.strip() for line in f if line.strip()]
            os.remove(temp_file)
        
        return tweets
    except Exception as e:
        print(f"Error fetching tweets for {username}: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return []

def main():
    handles_file = 'x_handles.txt'
    output_file = 'all_tweets.txt'
    usernames = read_usernames(handles_file)
    since_date = input('Enter the start date (YYYY-MM-DD): ').strip()
    all_tweets = []
    
    for username in usernames:
        print(f"Fetching tweets for {username}...")
        tweets = fetch_tweets(username, since_date)
        all_tweets.extend([tweet for tweet in tweets if tweet])
    
    # Write all tweets to output file as plain text
    with open(output_file, 'w', encoding='utf-8') as f:
        for tweet in all_tweets:
            f.write(tweet + '\n')
    print(f"Done. All tweets saved to {output_file}.")

if __name__ == '__main__':
    main()
