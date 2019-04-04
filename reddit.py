import praw
import re
import functions
import requests
import json
from api_key import id, secret

# ID : kgl9LR-fg9np6g
# secret: RCGhO6ruurRKslulwwY8yV5Xns8

reddit = praw.Reddit(client_id=id,
                     client_secret=secret,
                     user_agent='reddit_to_twitter')


#imgur pic
full_link = 'https://www.reddit.com/r/pics/comments/b9c569/such_a_beautiful_cat/'
#imgur gif/mp4
# full_link = 'https://www.reddit.com/r/holdmyfries/comments/avvow8/hmf_while_i_dance_with_my_t_rex_in_a_terrifying/'
grab_id = re.search(r'(?<=comments/).\w*', full_link)
topic_id = grab_id.group(0)

submission = reddit.submission(id=topic_id)
url = submission.url


if 'gfycat.com' in url:
    print('gfycat.com')
    gfycat_json = 'https://api.gfycat.com/v1/gfycats/' + url.rsplit('/', 1)[1]
    request = requests.get(gfycat_json).text
    json_request = json.loads(request)
    gif_5mb = json_request['gfyItem']['max5mbGif']
    #TODO download gif_5mb

elif 'redd.it' in url:

    print('Link redd.it')
    extension = url.rsplit('.', 1)[1]
    if extension == 'jpg':
        #TODO download jpg image
        print('jpg')
    else:
        id = url.rsplit('/', 1)[1]
        functions.save_vid(id)

elif 'imgur.com' in url:
    print('Link imgur.com')

    extension = url.rsplit('.', 1)[1]
    if extension == 'jpg':
        functions.save_jpg(url)
    else:
        print(url)
        # TODO download GIF as gif_tmp




