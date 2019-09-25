import reddit_handler
import twitter_handler
import functions
from time import sleep
from telegram_bot import Telegram


def text_messages(option, env=''):
    """ This function returns the corresponding answer messages to be sent for user through Telegram bot. """
    if option == 1:
        return 'Action Reddit to Twitter process cancelled by user.'
    elif option == 2:
        return 'Reddit link received. Please choose account to make upload, type "DEV" for test account or "PROD" for ' \
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
    message_to_be_sent = ''

    while True:
        # Always check if connection is active first to avoid errors and exceptions
        functions.check_internet_loop()

        last_updates = bot.get_updates()

        for update in last_updates:
            update_data = bot.get_update_data(update['message'])

            # Debugs
            # print(update_data['id'])
            # print(update_data['user'])

            # TODO make a new check because if there is in the URL the 'CANCEL' word this would trigger this IF
            if 'CANCEL' in update_data['text']:
                message_to_be_sent = text_messages(1)
                link_received = 0
                reddit_link = ''

            elif reddit_link and ready_to_tweet:
                print('Reddit link received and account to tweet selected. Making the magic happen.')
                message_to_be_sent = action(reddit_link, update_data['text'], env)
                link_received = 0
                ready_to_tweet = 0
                reddit_link = ''

            elif 'reddit.com' in update_data['text'] and link_received == 0:
                message_to_be_sent = text_messages(2)
                link_received = 1
                reddit_link = update_data['text']

            # grabs message text to be sent on tweet alongside media content
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
    # Message to deliver to Telegram chat from return of the tweet functions
    tweet_return = ''
    saved_file_type = reddit_handler.download_reddit_submission(full_link)

    print('Type of file saved from Reddit post => ' + saved_file_type)

    # Depending on file format, different functions are used
    if saved_file_type == 'gif' or saved_file_type == 'jpg':
        tweet_return = twitter_handler.tweeet_image(tweet_msg, saved_file_type, env)
    elif saved_file_type == 'mp4':
        tweet_return = twitter_handler.tweet_video(tweet_msg, env)
    return tweet_return


# Python main or modular check
if __name__ == '__main__':
    # Check connection before initializing class
    functions.check_internet_loop()

    bot = Telegram()
    bot.get_me()
    main()
