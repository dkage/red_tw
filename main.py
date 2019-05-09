import reddit_handler
import twitter_handler
from time import sleep
from telegram_bot import Telegram


def text_messages(option, env=''):
    """ This function returns the corresponding message to be sent for user through Telegram bot. """
    if option == 1:
        return 'Action Reddit to Twitter process cancelled by user.'
    elif option == 2:
        return 'Reddit link received. Please choose account to make upload, type "DEV" for test account or "PROD" for '\
               'main account.'
    elif option == 3:
        return 'Type tweet text message. The next message sent will be tweeted alongside the media from the given ' \
               'link.\n' \
               'The typed message will be sent using Twitter profile set as {} environment'.format(env)
    return 'INVALID OPTION'


def main():
    """Keeps script running and getting new telegram bot updates"""

    link_received = 0
    ready_to_tweet = 0
    reddit_link = ''
    env = ''

    while True:
        last_updates = bot.get_updates()

        for update in last_updates:
            update_data = bot.get_update_data(update['message'])

            # Debugs
            # print(update_data['id'])
            # print(update_data['user'])
            # bot.send_message(update_data['text'], update_data['id)

            if 'CANCEL' in update_data['text']:
                message_to_be_sent = text_messages(1)
                link_received = 0
                reddit_link = ''

            elif reddit_link and ready_to_tweet:
                message_to_be_sent = action(reddit_link, update_data['text'], env)
                link_received = 0
                reddit_link = ''

            elif 'reddit.com' in update_data['text'] and link_received == 0:
                message_to_be_sent = text_messages(2)
                link_received = 1
                reddit_link = update_data['text']

            elif ('DEV' in update_data['text'] or 'dev' in update_data['text']) or \
                    ('PROD' in update_data['text'] or 'prod' in update_data['text']) and link_received == 1:
                message_to_be_sent = text_messages(3, update_data['text'])
                ready_to_tweet = 1
                env = update_data['text']

            else:
                message_to_be_sent = 'Invalid command, please try again.'

            bot.send_message(message_to_be_sent, update_data['id'], update_data['user'])
        sleep(1)


def action(full_link, tweet_msg, env):
    # tweet_msg = 'Test ' + str(datetime.datetime.now())
    saved_file_type = reddit_handler.download_reddit_submission(full_link)

    print('saved_file_type = ' + saved_file_type)
    if saved_file_type == 'gif' or saved_file_type == 'jpg':
        return twitter_handler.tweeet_image(tweet_msg, saved_file_type, env)
    elif saved_file_type == 'mp4':
        return twitter_handler.tweet_video(tweet_msg, env)


# Python main or modular check
if __name__ == '__main__':
    bot = Telegram()
    bot.get_me()
    main()
