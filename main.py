import reddit_handler
import twitter_handler
import datetime
from telegram_bot import Telegram

bot = Telegram()
bot.get_me()

last_updates = bot.get_updates()
for update in last_updates:
    update_text, update_chat_id, update_from_user = bot.get_update_data(update['message'])
    print(update_text)
    print(update_chat_id)
    print(update_from_user)





# tweet_msg = 'Test ' + str(datetime.datetime.now())
# saved_file_type = reddit_handler.download_reddit_submission(full_link)
#
# print('saved_file_type = ' + saved_file_type)
# if saved_file_type == 'gif' or saved_file_type == 'jpg':
#     twitter_handler.tweeet_image(tweet_msg, saved_file_type)
# elif saved_file_type == 'mp4':
#     twitter_handler.tweet_video(tweet_msg)
