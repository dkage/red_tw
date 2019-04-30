import os
import sys
from TwitterAPI import TwitterAPI
# Prod Keys
from api_keys import twitter_id, twitter_secret, twitter_access_token, twitter_access_secret
# Dev Keys
from api_keys import twitter_id_dev, twitter_secret_dev, twitter_access_token_dev, twitter_access_secret_dev


def api_setup(env_variable):
    """
    This function grabs the environment passed from user on Telegram bot, and use the corresponding keys
    depending on the account being used. Ideally you should use a Twitter account for tests initially to check
    for errors depending on the type of media to be uploaded.
    """

    if env_variable == 'DEV':
        api_env = TwitterAPI(twitter_id_dev,
                             twitter_secret_dev,
                             twitter_access_token_dev,
                             twitter_access_secret_dev)
    elif env_variable == 'PROD':
        api_env = TwitterAPI(twitter_id,
                             twitter_secret,
                             twitter_access_token,
                             twitter_access_secret)
    else:
        api_env = 'Invalid'
    return api_env


def tweet_video(tweet_text, env):
    """This function tweets video files (mp4 format)"""

    video_filename = './tmp/tmp.mp4'

    def check_status(r):
        # EXIT PROGRAM WITH ERROR MESSAGE
        if r.status_code < 200 or r.status_code > 299:
            print(r.status_code)
            print(r.text)
            sys.exit(0)

    # Set API keys depending on environment to be used for tweet
    api = api_setup(env.upper())
    if api == 'invalid':
        return 'Invalid environment called'

    bytes_sent = 0
    total_bytes = os.path.getsize(video_filename)
    file = open(video_filename, 'rb')

    upload_return = api.request('media/upload',
                                {'command': 'INIT', 'media_type': 'video/mp4', 'total_bytes': total_bytes})
    check_status(upload_return)

    media_id = upload_return.json()['media_id']
    segment_id = 0

    while bytes_sent < total_bytes:
        chunk = file.read(4*1024*1024)
        upload_return = api.request('media/upload',
                                    {'command': 'APPEND', 'media_id': media_id, 'segment_index': segment_id},
                                    {'media': chunk})
        check_status(upload_return)
        segment_id = segment_id + 1
        bytes_sent = file.tell()
        print('[' + str(total_bytes) + ']', str(bytes_sent))

    upload_return = api.request('media/upload',
                                {'command': 'FINALIZE', 'media_id': media_id})
    check_status(upload_return)

    upload_return = api.request('statuses/update',
                                {'status': tweet_text, 'media_ids': media_id})
    check_status(upload_return)


def tweeet_image(tweet_text, file_type, env):
    """This function tweets image files (gifs and jpgs formats)"""

    # Calls API for the chosen account
    api = api_setup(env.upper())
    if api == 'invalid':
        return 'Invalid environment called'

    image_path = './tmp/tmp.' + file_type

    # Upload image using the API
    file = open(image_path, 'rb')
    data = file.read()
    api_response = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if api_response.status_code == 200 else 'UPLOAD MEDIA FAILURE: ' + api_response.text)

    # Post tweet with a reference to uploaded image alongside the chosen text only if media was successfully uploaded
    if api_response.status_code == 200:
        media_id = api_response.json()['media_id']
        api_response = api.request('statuses/update', {'status': tweet_text, 'media_ids': media_id})
    else:
        return 'Error during media upload: ' + api_response.text
    print('UPDATE STATUS SUCCESS' if api_response.status_code == 200 else 'UPDATE STATUS FAILURE: ' + api_response.text)
