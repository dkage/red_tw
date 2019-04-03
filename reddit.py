import praw
import requests
import json
from api_key import id, secret

# ID : kgl9LR-fg9np6g
# secret: RCGhO6ruurRKslulwwY8yV5Xns8

reddit = praw.Reddit(client_id=id,
                     client_secret=secret,
                     user_agent='reddit_to_twitter')


# gfycat.com
submission = reddit.submission(id='b7j480')
# redd.it
# submission = reddit.submission(id='b8rkr1')
# imgur
# submission = reddit.submission(id='b8uf7e')


url = submission.url


if 'gfycat.com' in url:
    print('gfycat.com')
    gfycat_json = 'https://api.gfycat.com/v1/gfycats/' + url.rsplit('/', 1)[1]
    request = requests.get(gfycat_json).text
    json_request = json.loads(request)
    gif_5mb = json_request['gfyItem']['max5mbGif']



elif 'redd.in' in url:
    print('Link redd.it')
    extension = url.rsplit('.', 1)[1]
    print(extension)
elif 'imgur.com' in url:
    print('Link imgur.com')
    extension = url.rsplit('.', 1)[1]
    print(extension)

