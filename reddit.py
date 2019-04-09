import praw
import re
import functions
import requests
import json
import os
from api_key import reddit_id, reddit_secret

# ID : kgl9LR-fg9np6g
# secret: RCGhO6ruurRKslulwwY8yV5Xns8

reddit = praw.Reddit(client_id=reddit_id,
                     client_secret=reddit_secret,
                     user_agent='reddit_to_twitter')


#############
## REDD.IT ##
#############
# REDD.IT # GIF/MP4
full_link = 'https://www.reddit.com/r/gifs/comments/b9etxb/ice_melting_off_a_handrail/'
# Redd.it # Mp4 sound
full_link = 'https://www.reddit.com/r/holdmybeer/comments/ban2nj/let_me_just_do_a_quick_backflip_off_this_table/'
# REDD.IT # JPG
# full_link = 'https://www.reddit.com/r/pics/comments/b9vhg9/long_exposure_of_a_shipwreck/'

###########
## IMGUR ##
###########
# IMGUR # GIFV # T-REX DANCING
# full_link = 'https://www.reddit.com/r/holdmyfries/comments/avvow8/hmf_while_i_dance_with_my_t_rex_in_a_terrifying/'
# full_link = 'https://www.reddit.com/r/gifs/comments/b9s44l/screams_in_cat_what_are_those/'
# IMGUR # JPG
# full_link = 'https://www.reddit.com/r/pics/comments/b9c569/such_a_beautiful_cat/'

############
## GFYCAT ##
############
# GFYCAT # GIF
# full_link = 'https://www.reddit.com/r/gifs/comments/b9qg8e/8_year_old_doing_a_double_backflip/'

grab_id = re.search(r'(?<=comments/).\w*', full_link)
topic_id = grab_id.group(0)

submission = reddit.submission(id=topic_id)
url = submission.url

saved_file_type = ''
if 'gfycat.com' in url:
    gfycat_json = 'https://api.gfycat.com/v1/gfycats/' + url.rsplit('/', 1)[1]
    request = requests.get(gfycat_json).text
    json_request = json.loads(request)
    gif_5mb = json_request['gfyItem']['max5mbGif']
    functions.save(gif_5mb, 'gif')
    saved_file_type = 'gif'


elif 'redd.it' in url:
    extension = url.rsplit('.', 1)[1]
    if extension == 'jpg':
        functions.save(url, 'jpg')
        saved_file_type = 'jpg'
    else:
        functions.save_vid(url)
        saved_file_type = 'mp4'


elif 'imgur.com' in url:
    url_breakdown = url.rsplit('.', 1)
    extension = url_breakdown[1]
    if extension == 'jpg':
        functions.save(url, 'jpg')
        saved_file_type = 'jpg'
    elif extension == 'gifv' or extension == 'mp4':
        url = url_breakdown[0] + '.mp4'
        functions.save(url, 'mp4')
        saved_file_type = 'mp4'


# TODO find a way to check size of the new file
# Max gif   - 15mb
# Max image -  5mb

filename = './tmp/tmp.' + saved_file_type
file_size = os.stat(filename).st_size


if saved_file_type == 'gif' and file_size < 15000000:
    print('gif accepted size')
if saved_file_type == 'jpg' and file_size < 5000000:
    print('jpg accepted size')

