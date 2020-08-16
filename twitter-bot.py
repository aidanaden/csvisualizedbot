import argparse
import tweepy
import emoji
from time import sleep
from credentials import *
from datetime import datetime




# get current & time 
def get_current_date_time():
  now = datetime.now()
  now_str = now.strftime("%d/%m/%Y %H:%M:%S")
  return now_str




def check_if_string_contains_emoji(string):
  has_emoji = bool(emoji.get_emoji_regexp().search(string))
  return has_emoji




# set up stuff for twitter bot to work
def setup_api():


  # authenticate twitter bot with consumer/developer key + secret
  # authorize access to app via access key + secret
  auth = tweepy.OAuthHandler(consumer_key=consumer_key,consumer_secret=consumer_secret)
  auth.set_access_token(access_token, access_secret)
  api = tweepy.API(auth_handler=auth)


  return api




# check if tweet can be considered inspirational
# (remove non-inspirational tweets)
def check_if_tweet_inspirational(status):

  
  # check if status/tweet contains urls
  # if it does, not considered an inspirational tweet
  if len(status.entities['urls']) > 0:
    return False
  
  
  # check if status/tweet is a reply
  # to another person's tweet
  if status.in_reply_to_user_id is not None:
    print(f'\nTweet is a reply to another tweet! Tweet written by {status.user.name}. Not gonna retweet!')
    return False


  # check if status/tweet is a quote
  # retweet/quote status
  if status.is_quote_status is True:
    print(f'\nTweet is a quote retweet! Tweet written by {status.user.name}. Not gonna retweet!')
    return False

  
  # check if tweet is a retweet
  if hasattr(status, 'retweeted_status') is True:
    print(f'\nTweet is a retweet! Original tweet was written by {status.retweeted_status.user.name}. Not gonna retweet!')
    return False

  
  if "?" in status.text:
    print(f'\nTweet contains "?"! Tweet written by {status.user.name}. Not gonna retweet!')
    return False


  if "#" in status.text:
    print(f'\nTweet contains "#"! Tweet written by {status.user.name}. Not gonna retweet!')
    return False

  
  if check_if_string_contains_emoji(status.text):
    print(f'\nTweet contains an emoji! Tweet written by {status.user.name}. Not gonna retweet!')
    return False

  
  if ('media' in status.entities):
    print(f'\nTweet contains media! Tweet written by {status.user.name}. Not gonna retweet!')
    return False
  

  # if passes all filters, tweet has 
  # been verified to be inspirational
  else:
    return True




# main code block to run twitter bot
def main():


  # set up api authentication
  api = setup_api()


  # visual graphic accounts to get inspiration from 
  # (will manually use bot to follow these accounts)
  inspiration_accounts = api.friends()


  # access latest tweets from inspiration accounts 
  while True:


    # print date n time current cycle started
    now = get_current_date_time()
    print(f'{now} SGT - Checking for inspirational tweets')


    # cycle thru each inspiration account
    for inspiration_acc in inspiration_accounts:
      

      # print current account being cycled through
      print(f'Currently at {inspiration_acc.name}\'s account\n')


      # cycle through latest 10 tweets from user (might need to fix in case user creates
      # more than 10 tweets fromt the last time we checked the account)
      for tweet in tweepy.Cursor(api.user_timeline, id=inspiration_acc.id, include_entities=True).items(10):

          
        # check if tweet is inspirational
        if check_if_tweet_inspirational(tweet):

          
          # if tweet is inspirational,
          # type text of tweet to console
          print('tweet is inspirational!')
          print(tweet.text) 


          # attempt to retweet inspirational tweet
          try:
            tweet.retweet()
            print(f'tweet retweeted!')


          # if error occurred while retweeting,
          # print reason of error
          except tweepy.TweepError as e:
            print(e.reason)


          # in case error of iterating over values
          # that do not exist, stop iterating
          except StopIteration:
            break
        
    
    # sleep for 10 mins before checking again
    sleep(600)




if __name__ == '__main__':
    main()