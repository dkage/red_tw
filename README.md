# Reddit to Twitter

This project was created to make easier to upload video files from Reddit directly to a Twitter account.

As Reddit posts with media (mp4, gif, jpg) are normally posted from different hosting services, and as each service uses different
file types, as often I want to post something I see interesting on Reddit to my Twitter account, I needed to handle many filetypes,
use online converter tools to get the right format/size for Twitter to upload, and only then share the media with my followers. 

To make this process a lot less painful I developed this little program that works as middle-man converter between Reddit and Twitter.
 
Still working in a lot of exception handling, but it works fine already most of the time.


As it uses a Telegram bot as a medium to get inputs (that way you have as your disposal at any time just by talking to it, no need to 
install app), you also need a bot key alongside the Twitter and Reddit ones for API usage.

To use it you just need to create a file in the same directory, called "api_keys.py" and insert your keys.

### api_keys.py example

```
# Telegram Bot API KEY
BOT_KEY = 'telegram_bot_key'


# Reddit API keys
reddit_secret = 'reddit_secret_key'
reddit_id = 'reddit_id_code'


# Twitter API keys # INSERT YOUR TEST ACCOUNT HERE (CALLED DEV) # OPTIONAL
twitter_id_dev = 'twitter_id_code'
twitter_secret_dev = 'twitter_secret_code'
twitter_access_token_dev = 'twitter_access_token'
twitter_access_secret_dev = 'twitter_access_secret'


# Twitter API keys # INSERT YOUR MAIN ACCOUNT HERE (CALLED PROD)
twitter_id = 'twitter_id_code'
twitter_secret = 'twitter_secret_code'
twitter_access_token = 'twitter_access_token'
twitter_access_secret = 'twitter_access_secret'
```

 ### How to use
 
... [will add instructions later]
