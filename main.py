import reddit_handler
import twitter_handler
import datetime
from time import sleep
from telegram_bot import Telegram


# Keeps script running and getting new updates
def main():
    link_received = 0
    ready_to_tweet = 0
    reddit_link = ''
    env = ''

    while True:
        last_updates = bot.get_updates()

        for update in last_updates:
            update_text, update_chat_id, update_from_user = bot.get_update_data(update['message'])
            # print(update_text)
            # print(update_chat_id)
            # print(update_from_user)
            # bot.send_message(update_text, update_chat_id)
            if 'cancel' in update:
                bot.send_message('Action Reddit to Twitter process cancelled by user.', update_chat_id)
                link_received = 0
                reddit_link = ''
            elif reddit_link and ready_to_tweet:
                action(reddit_link, update, env)
            elif 'reddit.com' in update_text and link_received == 0:
                bot.send_message('Reddit link received. Please choose account to make upload, type DEV for test account'
                                 ' or type PROD for main account.', update_chat_id)
                link_received = 1
                reddit_link = update_text
            elif 'DEV' in update_text and link_received == 1:
                bot.send_message('Type the message to be tweeted alongside the media from Reddit', update_chat_id)
                ready_to_tweet = 1
                env = 'DEV'
            elif 'PROD' in update_text and link_received == 1:
                bot.send_message('Type the message to be tweeted alongside the media from Reddit', update_chat_id)
                ready_to_tweet = 1
                env = 'PROD'
            else:
                bot.send_message('Invalid command', update_chat_id)

        sleep(1)


def action (full_link, tweet_msg, env):
    # tweet_msg = 'Test ' + str(datetime.datetime.now())
    saved_file_type = reddit_handler.download_reddit_submission(full_link)

    print('saved_file_type = ' + saved_file_type)
    if saved_file_type == 'gif' or saved_file_type == 'jpg':
        twitter_handler.tweeet_image(tweet_msg, saved_file_type, env)
    elif saved_file_type == 'mp4':
        twitter_handler.tweet_video(tweet_msg, env)


# Python main or modular check
if __name__ == '__main__':
    bot = Telegram()
    bot.get_me()
    main()



