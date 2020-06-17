#import pandas as pd
#import numpy as np
import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("2xxVGD18npYidiG1IDpz1PSGF", "aYocWtYkBkhH03P0fjfSo2zLpwLC8B4Idm9VT1aJfDqc6YRvRU")
auth.set_access_token("1005727485831479296-FEUSmzBYlUcoyN9iJJoBnkfNL9OotI","45wNdlmpwtF9rsG9dtPNefs1O0xS9nSWZ7N04ialeBSVh")
api = tweepy.API(auth, wait_on_rate_limit=True)
# test authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    
dt = pd.DataFrame(columns = ['Tweets', 'User','User_location','fav_count', 'rt_count', 'tweet_date'])


''' Same for the other hashtags #IndiaFightsCorona & #IndiaLockdown
    We collected the twitter data on day to day basis.'''

i = 0
# tweepy api call
for tweet in tweepy.Cursor(api.search, q="#COVID19India", count=100, lang='en').items(): 
  print(i, end='\r')
  dt.loc[i, 'Tweets'] = tweet.text
  dt.loc[i, 'User_location'] = tweet.user.location
  dt.loc[i, 'tweet_date'] = tweet.created_at
  i+=1
  if i == 100:
    break
  else:
    pass


#Look at the first five rows of the data
dt.head()

#save data csv file in the root folder
dt.to_csv("Data/tweet_#Covid19Indianew_.csv",index=False)
