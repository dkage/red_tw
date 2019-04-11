import reddit_handler
import twitter_handler
import datetime

#############
## REDD.IT ##
#############
# REDD.IT # GIF/MP4
# full_link = 'https://www.reddit.com/r/gifs/comments/b9etxb/ice_melting_off_a_handrail/'
# Redd.it # Mp4 sound
# full_link = 'https://www.reddit.com/r/holdmybeer/comments/ban2nj/let_me_just_do_a_quick_backflip_off_this_table/'
# REDD.IT # JPG
# full_link = 'https://www.reddit.com/r/pics/comments/b9vhg9/long_exposure_of_a_shipwreck/'
#jpg
# full_link = 'https://www.reddit.com/r/pics/comments/bblifz/this_is_what_bone_cancer_looks_like/'
#gif
# full_link = 'https://www.reddit.com/r/gifs/comments/bbfsio/pretending_to_punch_the_haunted_centaur/'
# full_link = 'https://www.reddit.com/r/gifs/comments/bbxy1l/live_shartting_accident/'

###########
## IMGUR ##
###########
# IMGUR # GIFV # T-REX DANCING
# full_link = 'https://www.reddit.com/r/holdmyfries/comments/avvow8/hmf_while_i_dance_with_my_t_rex_in_a_terrifying/'
# full_link = 'https://www.reddit.com/r/gifs/comments/b9s44l/screams_in_cat_what_are_those/'
# IMGUR # JPG
# full_link = 'https://www.reddit.com/r/pics/comments/b9c569/such_a_beautiful_cat/'

############
## GFYCAT ##
############
# GFYCAT # GIF
# full_link = 'https://www.reddit.com/r/gifs/comments/b9qg8e/8_year_old_doing_a_double_backflip/'
full_link = 'https://www.reddit.com/r/holdmybeer/comments/babyef/hmb_while_i_swing_my_huge_hammer/'


tweet_msg = 'Test ' + str(datetime.datetime.now())
saved_file_type = reddit_handler.download_reddit_submission(full_link)

print('saved_file_type = ' + saved_file_type)
if saved_file_type == 'gif' or saved_file_type == 'jpg':
    twitter_handler.tweeet_image(tweet_msg, saved_file_type)
elif saved_file_type == 'mp4':
    twitter_handler.tweet_video(tweet_msg)
