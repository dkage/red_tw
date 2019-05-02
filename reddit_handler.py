import praw
import re
import functions
import requests
import json
from api_keys import reddit_id, reddit_secret


def download_reddit_submission(full_link):
    reddit = praw.Reddit(client_id=reddit_id,
                         client_secret=reddit_secret,
                         user_agent='reddit_to_twitter')



    grab_id = re.search(r'(?<=comments/).\w*', full_link)
    print(grab_id)
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

    return saved_file_type


# TODO find a way to check size of the new file
# Max gif   - 15mb
# Max image -  5mb

# filename = './tmp/tmp.' + saved_file_type
# file_size = os.stat(filename).st_size
#
#
# if saved_file_type == 'gif' and file_size < 15000000:
#     print('gif accepted size')
# if saved_file_type == 'jpg' and file_size < 5000000:
#     print('jpg accepted size')
#
