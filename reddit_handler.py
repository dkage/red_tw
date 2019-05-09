import praw
import re
import functions
import requests
import json
from api_keys import reddit_id, reddit_secret


def download_reddit_submission(full_link):

    # Sets reddit API keys
    reddit = praw.Reddit(client_id=reddit_id,
                         client_secret=reddit_secret,
                         user_agent='reddit_to_twitter')

    # Grab reddit ID of given link for the API uses it to grab the reddit topic
    grab_id = re.search(r'(?<=comments/).\w*', full_link)
    topic_id = grab_id.group(0)

    # Uses the API to retrieve the link submitted in topic (image, gif or video)
    submission = reddit.submission(id=topic_id)
    url = submission.url

    # Discovers the file type based on the service it's uploaded on
    saved_file_type = ''
    if 'gfycat.com' in url:
        # Knowing that gfycat only has gifs, using service API grabs the version that has 5mb or less.
        gfycat_json = 'https://api.gfycat.com/v1/gfycats/' + url.rsplit('/', 1)[1]
        request = requests.get(gfycat_json).text
        json_request = json.loads(request)
        gif_5mb = json_request['gfyItem']['max5mbGif']

        # Downloads gif and sets file type to GIF
        functions.download(gif_5mb, 'gif')
        saved_file_type = 'gif'

    elif 'redd.it' in url:
        # If it's hosted on reddit can be either a jpg or mp4 (only formats used there)
        extension = url.rsplit('.', 1)[1]

        # Knowing the right extension to name the file, downloads it
        if extension == 'jpg':
            functions.download(url, 'jpg')
            saved_file_type = 'jpg'
        else:
            functions.download_video(url)
            saved_file_type = 'mp4'

    elif 'imgur.com' in url:
        # If it's hosted on imgur the possible extensions are JPG and GIFV/MP4 (both can be saved as mp4 file)
        url_breakdown = url.rsplit('.', 1)
        extension = url_breakdown[1]
        if extension == 'jpg':
            functions.download(url, 'jpg')
            saved_file_type = 'jpg'
        elif extension == 'gifv' or extension == 'mp4':
            url = url_breakdown[0] + '.mp4'
            functions.download(url, 'mp4')
            saved_file_type = 'mp4'

    return saved_file_type
