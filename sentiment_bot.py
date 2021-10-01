import json
import sys

import praw
from prawcore.exceptions import Forbidden

from bot_funcs import fetch_comments, process_comments, reply

# pass json file with api keys and bot account info
cert_file = sys.argv[1]
with open(cert_file, 'r') as f:
    data = json.load(f)

client_id = data['client_id']
secret = data['secret']
username = data['username']
password = data['password']
user_agent = data['user_agent']

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=secret,
    user_agent=user_agent,
    username=username,
    password=password
)


def process(mention):
    '''
    Gathers comments from parent author,
    and passes them on for processing and reply
    '''
    author = mention.author
    parent_author = mention.parent().author
    print(f'/u/{author} wants to see if /u/{parent_author} is having a bad day...')
    comments = fetch_comments(parent_author)
    num_comments = len(comments)
    avg_score = process_comments(comments, num_comments)
    reply(mention, parent_author, avg_score, num_comments)


# get 10 most recent messages
mentions = list(reddit.inbox.unread(limit=10))

if len(mentions) > 0:
    for mention in mentions:
        print(mention.body)
        if username in mention.body:
            try:
                process(mention)
            except (AttributeError, Forbidden):
                print('Something went wrong with comment id:', mention.id)

    reddit.inbox.mark_read(mentions)
else:
    print('No new comments.')
