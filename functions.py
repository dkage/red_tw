import os
import requests
from moviepy.editor import *

directory = './tmp/'
user_agent1 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'


if not os.path.exists(directory):
    os.makedirs(directory)


def save(url, extension):
    """This function receives an URL ending with a file extension and saves that file (gif, jpg)"""
    name = 'tmp.' + extension
    full_file_path = directory + name

    try:
        image_request = requests.get(url, headers={'User-Agent': user_agent1})
        if image_request.status_code == 200:
            with open(full_file_path, 'wb') as file:
                file.write(image_request.content)
        print('File downloaded successfully')
    except Exception as error:
        print('Error accessing URL:\n' + str(error))

    return True


def save_vid(video_url):
    """This function is used to save specific cases where video/gif is hosted in redd.it"""
    name = 'tmp.mp4'
    full_file_path = directory + name

    url_mp4 = video_url + '/DASH_480'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/70.0.3538.77 Safari/537.36'
    response = requests.get(url_mp4, headers={'User-Agent': user_agent})

    with open(full_file_path, 'wb') as f:
        print("Downloading chunck")
        for chunk in response.iter_content(chunk_size=255):
            if chunk:
                f.write(chunk)
    return True


def convert_mp4_to_gif(video_file='./tmp/tmp.mp4'):
    """This function receives a MP4 filename with its relative path and converts it to GIF"""
    # Create object with mp4 file
    new_gif = (VideoFileClip(video_file))
    valid = False
    while valid:
        valid = True
    new_gif.write_gif("./tmp/tmp1.gif", program='ffmpeg', fps=new_gif.fps - 19)

    return True


def check_size():
    # TODO create function to check gif and jpg size before sending to Twitter
    return True



