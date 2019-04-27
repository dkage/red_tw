from api_keys import BOT_KEY
import requests


class Telegram:

    def __init__(self):

        self.url = "https://api.telegram.org/bot{}/".format(BOT_KEY)

        self.name = ''
        self.bot_id = 0
        self.offset = None
        self.aux = 0
        self.updates_json = ''

    def get_me(self):
        http_response = requests.get(self.url+'getMe')
        json_response = http_response.json()
        self.bot_id = json_response['result']['id']
        self.name = json_response['result']['username']
        if json_response['ok']:
            return True
        else:
            return False

    def get_updates(self):
        update_url = self.url + 'getUpdates?timeout=100'
        # If offset is already set, concatenates it to tell API last ID already received
        if self.offset:
            update_url += "&offset={}".format(self.offset)
        http_response = requests.get(update_url)
        json_response = http_response.json()
        self.updates_json = json_response['result']
        # print(update_url)  # Keep for debugging
        # print(json_response)  # Keep for debugging
        # Grabs last offset update_id, and adds one so updates already received and not returned anymore
        # if json_response['result'][-1]['update_id']:
        if json_response['result']:
            self.offset = int(json_response['result'][-1]['update_id']) + 1
        if json_response['ok']:
            return json_response['result']
        else:
            return False

    @staticmethod
    def get_update_data(json_update):

        update_text = json_update['text']
        update_chat_id = json_update['from']['id']
        update_from_user = json_update['from']['username']

        if not update_text or not update_chat_id:
            return False
        else:
            return update_text, update_chat_id, update_from_user

    def send_message(self, text_to_send, receiver_id):
        http_response = requests.get(self.url + "sendMessage?text={}&chat_id={}".format(text_to_send, receiver_id))
        if http_response.status_code == 200:
            return True
        else:
            return False


