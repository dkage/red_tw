import os
import sys
from TwitterAPI import TwitterAPI
from api_keys import twitter_id, twitter_secret, twitter_access_token, twitter_access_secret


def tweet_video(tweet_text):
    """This function tweets video files (mp4 format)"""

    video_filename = './tmp/tmp.mp4'

    def check_status(r):
        # EXIT PROGRAM WITH ERROR MESSAGE
        if r.status_code < 200 or r.status_code > 299:
            print(r.status_code)
            print(r.text)
            sys.exit(0)

    api = TwitterAPI(twitter_id,
                     twitter_secret,
                     twitter_access_token,
                     twitter_access_secret)

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


def tweeet_image(tweet_text, file_type):
    """This function tweets image files (gifs and jpgs formats)"""

    image_path = './tmp/tmp.' + file_type

    api = TwitterAPI(twitter_id,
                     twitter_secret,
                     twitter_access_token,
                     twitter_access_secret)

    # STEP 1 - upload image
    file = open(image_path, 'rb')
    data = file.read()
    r = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE: ' + r.text)

    # STEP 2 - post tweet with a reference to uploaded image
    if r.status_code == 200:
        media_id = r.json()['media_id']
        r = api.request('statuses/update', {'status': tweet_text, 'media_ids': media_id})
    print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE: ' + r.text)