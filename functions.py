import requests


def save_vid(video_id=None):

    name = 'video_tmp.mp4'
    url_mp4 = 'https://v.redd.it/' + video_id + '/DASH_480'

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/70.0.3538.77 Safari/537.36'
    response = requests.get(url_mp4, headers={'User-Agent': user_agent})

    with open(name, 'wb') as f:
        print("Downloading chunck")
        for chunk in response.iter_content(chunk_size=255):
            if chunk:
                f.write(chunk)
    return True


def save_jpg(url):

    name = 'image_tmp.jpg'

    try:
        image_request = requests.get(url)
        if image_request.status_code == 200:
            with open(name, 'wb') as file:
                file.write(image_request.content)
        print('Image downloaded successfully')
    except Exception as error:
        print('Error accessing URL:\n' + error)




    return True