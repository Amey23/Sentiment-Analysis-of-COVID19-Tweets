import numpy as np
import pandas as pd


df1 = pd.read_csv("my_tweets_IFC.csv",encoding='latin1')
df1 = pd.DataFrame({'Tweets':df1['Tweets'], 'tweet_date':df1['tweet_date'], 'User_location':df1['User_location']})
#df1.head()


df2 = pd.read_csv("tweets_IFC_28.csv",encoding='latin1')
df2 = pd.DataFrame({'Tweets':df2['Tweets'], 'tweet_date':df2['tweet_date'], 'User_location':df2['User_location']})
#df2.head()


df3 = pd.read_csv("tweets_COVID19_28.csv",encoding='latin1')
df3 = pd.DataFrame({'Tweets':df3['Tweets'], 'tweet_date':df3['tweet_date'], 'User_location':df3['User_location']})
#df3.head()


df4 = pd.read_csv("tweets_COVID19India_2000.csv",encoding='latin1')
df4 = pd.DataFrame({'Tweets':df4['Tweets'], 'tweet_date':df4['tweet_date'], 'User_location':df4['User_location']})
#df4.head()


df5 = pd.read_csv("tweets_LD_2000.csv",encoding='latin1')
df5 = pd.DataFrame({'Tweets':df5['Tweets'], 'tweet_date':df5['tweet_date'], 'User_location':df5['User_location']})
#df5.head()


df6 = pd.read_csv("tweet_IFC_1_.csv",encoding='latin1')
df6 = pd.DataFrame({'Tweets':df6['Tweets'], 'tweet_date':df6['tweet_date'], 'User_location':df6['User_location']})
#df6.head()


df7 = pd.read_csv("tweet_LD_1_.csv",encoding='latin1')
df7 = pd.DataFrame({'Tweets':df7['Tweets'], 'tweet_date':df7['tweet_date'], 'User_location':df7['User_location']})
#df7.head()


df8 = pd.read_csv("tweet_COVID19_1_.csv",encoding='latin1')
df8 = pd.DataFrame({'Tweets':df8['Tweets'], 'tweet_date':df8['tweet_date'], 'User_location':df8['User_location']})
#df8.head()


df9 = pd.read_csv("tweet_UnlockIndia_1_.csv",encoding='latin1')
df9 = pd.DataFrame({'Tweets':df9['Tweets'], 'tweet_date':df9['tweet_date'], 'User_location':df9['User_location']})
#df9.head()


df10 = pd.read_csv("tweet_#UnlockLDnew_.csv",encoding='latin1')
df10 = pd.DataFrame({'Tweets':df10['Tweets'], 'tweet_date':df10['tweet_date'], 'User_location':df10['User_location']})
#df10.head()


df11 = pd.read_csv("tweet_#IFC5000_.csv",encoding='latin1')
df11 = pd.DataFrame({'Tweets':df11['Tweets'], 'tweet_date':df11['tweet_date'], 'User_location':df11['User_location']})
#df11.head()


df12 = pd.read_csv("tweet_#FailedLD_.csv",encoding='latin1')
df12 = pd.DataFrame({'Tweets':df12['Tweets'], 'tweet_date':df12['tweet_date'], 'User_location':df12['User_location']})
#df12.head()


df13 = pd.read_csv("tweet_#Covid19Indianew_.csv",encoding='latin1')
df13 = pd.DataFrame({'Tweets':df13['Tweets'], 'tweet_date':df13['tweet_date'], 'User_location':df13['User_location']})
#df13.head()


frames = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13]
result = pd.concat(frames)
result = result.drop_duplicates()
result.to_csv("IBM_SA_Tweets.csv", index=False)
