# Reddit to Twitter

This project was created to make easier to upload video files from reddit directly to Twitter.

As Reddit files comes from different services and formats, and for each type of file from each host I needed a different
website or service/application to download, I decided to create a code to make that easier.

Still working in a lot of exception handling, but it works fine already most of the time.


As it uses a Telegram bot as a medium (that way you have as your disposal at any time just by talking to it, no need to 
install app), you also need a bot key alongside the Twitter and Reddit ones for API usage.


To use it you just need to create a file in the same directory, called "api_keys.py" and insert your keys.

### api_keys.py example

```
# Telegram Bot API KEY
BOT_KEY = 'telegram_bot_key'


# Reddit API keys
reddit_secret = 'reddit_secret_key'
reddit_id = 'reddit_id_code'


# Twitter API keys # INSERT YOUR TEST ACCOUNT HERE (CALLED DEV)
twitter_id_dev = '***REMOVED***'
twitter_secret_dev = '***REMOVED***'
twitter_access_token_dev = '***REMOVED***'
twitter_access_secret_dev = '***REMOVED***'


# Twitter API keys # INSERT YOUR MAIN ACCOUNT HERE (CALLED PROD)
twitter_id = 'twitter_id_code'
twitter_secret = 'twitter_secret_code'
twitter_access_token = 'twitter_access_token'
twitter_access_secret = 'twitter_access_secret'
```

 

