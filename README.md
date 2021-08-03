# Reddit Sentiment Bot

This repo contains the code behind my Reddit bot, /u/bad_day_checker. This project was created to explore the Reddit API and the `vaderSentiment` package in Python. The idea was to have a bot that one could call to get a report on whether another individual on Reddit is always negative or they may just be having a bad day. Here is an example:

[img](link)

### How it works

The bot uses the `praw` (Python Reddit API Wrapper) package to access the Reddit API through objects and function calls. 

It begins with the bot being "summoned" via a comment (see the above example). The summon shows up as a message/mention in the bot account's inbox. From there, the bot goes to the comment that summoned them, the child, and retrieves information about the comment that was replied to, the parent. From the parent comment, it grabs the author's username. Using that username, it calls on `praw` to retrieve the user's 1,000 most recent comments from the Reddit API.

Once it collects these comments from the parent comment's author, the bot processes them all through `vaderSentiment`'s `SentimentIntensityAnalyzer`. This gives each comment a score between -1 and 1. Finally, it calculates the average of the sentiment scores and creates a report accordingly. If the average is positive it determines the parent comment author may just be having a bad day, otherwise it determines they are consistently sour.

### Other details

- The bot is running on a RaspberryPi Zero W and is launched every 30 minutes via CRON
- Only a max of 10 new summons are processed per run
- This repo/project is a slow work in progress

---

### Todo:

- [ ] Separate sentiment analyses of the parent comment from the rest of that user's comments used in averaging. Report both scores for reference.
- [ ] Add more positive and negative replies for the bot to choose from
- [ ] Add reporting of median sentiment (possibly replace average)
- [x] Fix bounds for positive/negative/neutral sentiments to be in line with VADER