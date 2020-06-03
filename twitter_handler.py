import os
from time import sleep
import sys
from TwitterAPI import TwitterAPI
# Prod Keys
from api_keys import twitter_id, twitter_secret, twitter_access_token, twitter_access_secret
# Dev Keys
from api_keys import twitter_id_dev, twitter_secret_dev, twitter_access_token_dev, twitter_access_secret_dev
from moviepy.editor import VideoFileClip


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


def check_api_status(r):
    # EXIT PROGRAM WITH ERROR MESSAGE IF API RETURN ERROR
    if r.status_code < 200 or r.status_code > 299:
        print('ERROR DURING API CONNECTION. Status code: ' + str(r.status_code))
        print(r.text)
        return False
    return True


def tweet_video(tweet_text, env):
    """This function tweets video files (mp4 format)"""

    video_filename = './tmp/tmp.mp4'

    clip_to_upload = VideoFileClip(video_filename)
    print('Clip length => ' + str(clip_to_upload.duration) + ' seconds')

    # Set API keys depending on environment to be used for tweet
    api = api_setup(env.upper())
    if api == 'invalid':
        return 'Invalid environment called'

    bytes_sent = 0
    total_bytes = os.path.getsize(video_filename)
    file = open(video_filename, 'rb')

    # Connection timeout increased to reduce errors that were happening because of slow connection to API (bad internet)
    api.CONNECTION_TIMEOUT = 20

    # Open request to start video upload
    # TODO read https://github.com/ttezel/twit/issues/306
    # TODO read https://github.com/ttezel/twit/issues/306
    # TODO read https://github.com/ttezel/twit/issues/306
    upload_return = api.request('media/upload',
                                {'command': 'INIT',
                                 'media_type': 'video/mp4',
                                 'media_category': 'tweet_video',
                                 'total_bytes': total_bytes})
    if not check_api_status(upload_return):
        return 'Error occurred during opening API upload request.'

    media_id = upload_return.json()['media_id']
    segment_id = 0

    while bytes_sent < total_bytes:
        chunk = file.read(4*1024*1024)
        upload_return = api.request('media/upload',
                                    {'command': 'APPEND', 'media_id': media_id, 'segment_index': segment_id},
                                    {'media': chunk})
        if not check_api_status(upload_return):
            return 'Error occurred during chunks uploading.'
        segment_id = segment_id + 1
        bytes_sent = file.tell()
        print('Total bytes to upload: [' + str(total_bytes) + '] \n Total bytes sent:', str(bytes_sent))

    upload_return = api.request('media/upload',
                                {'command': 'FINALIZE',
                                 'media_id': media_id})

    # Check for HTTP response errors code
    if not check_api_status(upload_return):
        return 'Error occurred when finalizing media upload.'

    print(upload_return.json())
    if upload_return.json()['processing_info']:
        while upload_return.json()['processing_info']['state'] is ('in_progress' or 'pending'):
            sleep(int(upload_return.json()['processing_info']['check_after_secs']))
            upload_return = api.request('media/upload',
                                        {'command': 'FINALIZE',
                                         'media_id': media_id})

    if upload_return.json()['processing_info']['state'] is 'failed':
        return 'Error occurred when processing video file on server side, error tw01'

    # Tweet!
    upload_return = api.request('statuses/update',
                                {'status': tweet_text, 'media_id': media_id})
    if not check_api_status(upload_return):
        return 'Error occurred sending tweet message alongside media uploaded.'
    else:
        return ' Media upload finished.\nTweet successfully sent.'


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

    # Post tweet with a reference to uploaded image alongside the chosen text only if media was successfully uploaded
    if api_response.status_code == 200:
        print('UPDATE STATUS SUCCESS')
        media_id = api_response.json()['media_id']
        api_response = api.request('statuses/update', {'status': tweet_text, 'media_ids': media_id})

        return 'Media uploaded successfully, tweet sent to API.$0D API return ' + api_response
    else:
        print('UPDATE STATUS FAILED. API response error ' + api_response)
        return 'Error during media upload: ' + api_response.text

