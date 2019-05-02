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

    # TODO make a CHECK case for video length ( MAX TWITTER API SIZE IS 30 SECONDS)
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
    """
    This function is used to save specific cases where video/gif is hosted in redd.it.
    The redd.it website loads two separated files, one for video and another for audio, this function downloads both of
    them and merges into a single video file with sound
    """

    name = 'tmp_video.mp4'
    name_audio = 'tmp_audio.mp4'
    video_file_path = directory + name
    audio_file_path = directory + name_audio
    output_file_path = directory + 'tmp.mp4'

    # Downloads MP4 in 480p resolution (gives the best file size to be uploaded later)
    url_mp4 = video_url + '/DASH_480'
    url_audio = video_url + '/audio'

    # User agent to be used during HTTP request
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/70.0.3538.77 Safari/537.36'

    # Download video file
    response = requests.get(url_mp4, headers={'User-Agent': user_agent})
    with open(video_file_path, 'wb') as f:
        print("Downloading video")
        for chunk in response.iter_content(chunk_size=255):
            if chunk:
                f.write(chunk)

    video_file_size = os.stat(video_file_path).st_size
    if video_file_size < 250:
        url_mp4 = video_url + '/DASH_360'
        response = requests.get(url_mp4, headers={'User-Agent': user_agent})
        with open(video_file_path, 'wb') as f:
            print("Downloading video")
            for chunk in response.iter_content(chunk_size=255):
                if chunk:
                    f.write(chunk)

    # Download audio file
    response = requests.get(url_audio, headers={'User-Agent': user_agent})
    with open(audio_file_path, 'wb') as f:
        print("Downloading audio")
        for chunk in response.iter_content(chunk_size=255):
            if chunk:
                f.write(chunk)

    audio_file_size = os.stat(audio_file_path).st_size

    mp4_video = (VideoFileClip(video_file_path))
    if audio_file_size > 243:
        # Loads video file as object using MOVIEPY into mp4_video variable and saves output as 'tmp.mp4'
        mp4_video.write_videofile(output_file_path, audio=audio_file_path)
    else:
        mp4_video.write_videofile(output_file_path)

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



