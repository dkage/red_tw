import praw
from api_key import id, secret

# ID : kgl9LR-fg9np6g
# secret: RCGhO6ruurRKslulwwY8yV5Xns8

reddit = praw.Reddit(client_id=id,
                     client_secret=secret,
                     user_agent='reddit_to_twitter')


# Gyf
submission = reddit.submission(id='b8hrx1')
# reddit
submission = reddit.submission(id='b8ls3t')
# imgur
submission = reddit.submission(id='b8cnob')

print(submission.url)
