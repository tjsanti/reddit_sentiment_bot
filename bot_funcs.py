import time

import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def fetch_comments(author):
    '''Gathers comments from Redditor instance'''

    return list(author.comments.new(limit=1_000))


def process_comments(comments, num_comments):
    '''Computes average sentiment score for an array of reddit Comments'''

    analyzer = SentimentIntensityAnalyzer()
    sum_scores = 0
    print(f'Processing {num_comments} comments')
    begin = time.time()

    for comment in comments:
        text = comment.body
        score = analyzer.polarity_scores(text)['compound']
        sum_scores += score

    end = time.time()
    avg_score = sum_scores / num_comments
    print(
        f'Finished in {end-begin:.3f} seconds. Average score {avg_score:.2f}')

    return avg_score


def reply(mention, parent_author, avg_score, num_comments):
    '''Replies to a reddit mention and then deletes it from the inbox'''

    positive_replies = [
        f"/u/{parent_author} might be having a bad day."
    ]
    negative_replies = [
        f"I think /u/{parent_author} might be a south pole elf."
    ]

    if avg_score > 0:
        opener = np.random.choice(positive_replies)
    else:
        opener = np.random.choice(negative_replies)

    score_report = f'\n\nTheir last {num_comments} comments had an average sentiment of {avg_score:.3f}.'

    if avg_score >= 0.05:
        score_report += ' (Pretty Positive)' + '\n'*4
    elif avg_score > -0.05:
        score_report += ' (Mostly Neutral)' + '\n'*4
    else:
        score_report += ' (Pretty Negative)' + '\n'*4

    signature = '___' + '\n\n' + \
        '^(I am a bot. If you believe there is an issue, please pm me so I can pass it on to my creator)'
    reply_comment = opener + score_report + signature
    mention.reply(reply_comment)
    mention.delete()
    print('Mention replied to and deleted')

    return
