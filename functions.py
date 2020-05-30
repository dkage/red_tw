import requests
from moviepy.editor import *
from urllib import request, error
from time import sleep
import os

directory = './tmp/'
user_agent1 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'


if not os.path.exists(directory):
    os.makedirs(directory)


def download(url, extension):
    """This function receives an URL ending with a file extension and saves that file (gif, jpg)"""
    name = 'tmp.' + extension
    full_file_path = directory + name

    print('\nDownloading {} file type, from url: {} \n'.format(extension, url))

    try:
        image_request = requests.get(url, headers={'User-Agent': user_agent1})
        if image_request.status_code == 200:
            with open(full_file_path, 'wb') as file:
                file.write(image_request.content)
        # TODO check if download was successful
        print('File downloaded successfully')
    except Exception as error:
        print('Error accessing URL:\n' + str(error))

    return True


def download_video(video_url):
    """
        This function is used to save specific cases where video/gif is hosted in redd.it. The redd.it website loads
        two separated files when url is accessed, one for video and another for audio, this function downloads both of
        them and merge into a single video file with sound output.
    :param video_url: url
    :return:
    """

    # TODO maybe create a new chat iteration if video length is too big, to ask for times to download video interval

    name = 'tmp_video.mp4'
    name_audio = 'tmp_audio.mp4'
    video_file_path = directory + name
    audio_file_path = directory + name_audio
    output_file_path = directory + 'tmp.mp4'

    # Downloads MP4 in 480p resolution
    # TODO needs to check size for each resolution version, to check the best quality possible within the API limits
    url_mp4 = video_url + '/DASH_1080'
    url_audio = video_url + '/audio'

    # User agent to be used during HTTP request
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/70.0.3538.77 Safari/537.36'

    # Download video file
    response = requests.get(url_mp4, headers={'User-Agent': user_agent})
    download_reddit_hosted(response, video_file_path, 'video')
    video_file_size = os.stat(video_file_path).st_size

    # If first try downloading video yields a file with less than 250 bytes, then it failed and the current video
    # URL needs the suffix with resolution number. This does not seem to be consistent, sometimes the first download
    # works, and sometimes it requires the /DASH_[resolution] added at the end.
    if video_file_size < 250:
        url_mp4 = video_url + '/DASH_1080'
        response = requests.get(url_mp4, headers={'User-Agent': user_agent})
        download_reddit_hosted(response, video_file_path, 'video')

    # Download audio file
    response = requests.get(url_audio, headers={'User-Agent': user_agent})
    download_reddit_hosted(response, audio_file_path, 'audio')
    audio_file_size = os.stat(audio_file_path).st_size

    mp4_video = (VideoFileClip(video_file_path))
    if audio_file_size > 243:
        # Loads video file as object using MOVIEPY into mp4_video variable and saves output as 'tmp.mp4'
        mp4_video.write_videofile(output_file_path, audio=audio_file_path)
    else:
        mp4_video.write_videofile(output_file_path)

    if mp4_video.duration > 30.00:
        # Duration must be between 0.5 seconds and 140 seconds
        # TODO needs to send message to user and return false to functions
        # TODO maybe create a new chat iteration if video length is too big, to ask for times to download video
        #  probably new function to be called

        print('Mp4 longer than 30 seconds limit')
        return False
    # TODO needs to check size, and if not download it again in lower res
    return True


def download_reddit_hosted(response, path, file_type):

    with open(path, 'wb') as f:
        print("Downloading " + file_type)
        for chunk in response.iter_content(chunk_size=255):
            if chunk:
                f.write(chunk)


def convert_mp4_to_gif(video_file='./tmp/tmp.mp4'):
    """This function receives a MP4 filename with its relative path and converts it to GIF"""
    # Create object with mp4 file
    new_gif = (VideoFileClip(video_file))
    valid = False
    while valid:
        valid = True
    new_gif.write_gif("./tmp/tmp1.gif", program='ffmpeg', fps=new_gif.fps - 19)

    return True


def check_size(filename, saved_file_type):

    # Max gif   - 15mb
    # Max image -  5mb

    filename = './tmp/tmp.' + saved_file_type
    file_size = os.stat(filename).st_size

    # Cases where size is too large for API return false, else goes to true
    if saved_file_type == 'gif' and file_size > 15728640:
        return False
    if saved_file_type == 'jpg' and file_size > 5242880:
        return False
    if saved_file_type == 'mp4' and file_size > 536870912:
        return False

    return True


def internet_on_check():
    """ Function used to check if machine running the script has internet connection online """
    try:
        # Tries urlopen on Google DNS IP because of reliable uptime and static address.
        request.urlopen('https://8.8.8.8/', timeout=10)
        return True
    except error.HTTPError as e:
        print(e.__dict__)
    except error.URLError as e:
        print(e.__dict__)
        return False


def check_internet_loop():
    # TODO this needs to be added alongside the entire project for each API request
    #  more tests are needed to check for more exceptions because of internet offline during
    while not internet_on_check():
        print('Internet connection is down. Retrying until Python detects that internet connection is online.')
        sleep(30)
    return True

