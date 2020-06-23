import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import string
from collections import Counter
#from nltk import stopwords
#stop = stopwords.words('english')
import re
import nltk
from pandas.api.types import is_numeric_dtype

DATA_URL = (
    "Dash_show_new.csv"
)
DATA1_URL = (
    "Emotions_India.csv"
)
DATA2_URL = (
    "geocode_new.csv"
)

st.title("Sentiment Analysis of COVID-19 Tweets")
st.sidebar.title("Sentiment Dashboard")
st.markdown("This application is a Streamlit dashboard used to analyze sentiments of COVID-19 tweets 🐦")
#st.sidebar.markdown("This application is a Streamlit dashboard used "
#           "to analyze sentiments of tweets 🐦")
 
st.text("")
@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    #dat['tweet_created'] = pd.to_datetime(dat['tweet_created'])
    return data

data = load_data()		
#st.markdown(data.shape)
#st.markdown(data.columns)
st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('Positive', 'Neutral', 'Negative'))
if not st.sidebar.checkbox("Hide", False):
    st.markdown("### Show random tweets by sentiment: %s" %(random_tweet))
    st.info(data.query("Sentiment == @random_tweet")[["Tweets"]].sample(n=1).iat[0,0])
	
st.text("")
st.sidebar.markdown("### Count of tweets by sentiment")
select = st.sidebar.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='1')
sentiment_count = data['Sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})
if not st.sidebar.checkbox("Close", False, key='2'):
    st.markdown("### Count of tweets by sentiment")
    st.success("Sentiment vs Tweets visualization helps us to analyse the sentiment of people's tweets. Mainly the sentiment of tweets are categorized into positive, negative or neutral based on the polarity score calculaated using Textblob library.")  
    st.text("Visualization Type: %s" %(select))
    if select == 'Bar plot':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)

@st.cache(persist=True)
def get_data():
    data = pd.read_csv(DATA1_URL)
    #dat['tweet_created'] = pd.to_datetime(dat['tweet_created'])
    return data
	
emt = get_data()
st.markdown("### Emotion Analysis of tweets")
st.success("Emotional analysis of tweets helps us to analyse the psychological state of people during the pandemic. As you see, most of the people are happy in the lockdown.")
fig_em = px.bar(emt, x='Emotion', y='Emotion_score', color='Emotion_score', width=800, height=500, title="Emotion Analysis Barplot showing count of Five emotions")
st.plotly_chart(fig_em)


st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('Positive', 'Neutral', 'Negative'))
if not st.sidebar.checkbox("Close", False, key='3'):
    st.subheader('Word cloud for sentiment: %s' % (word_sentiment))
    st.success("Word Cloud is a data visualization technique used for representing text data in which the size of each word indicates its frequency or importance. Significant textual data points can be highlighted using a word cloud.")
    df = data[data['Sentiment']==word_sentiment]
    df['Clean_tweets'] = df['Clean_tweets'].str.replace('\d+', '')
    df = df.astype(str)
    words = ' '.join(df['Clean_tweets'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=900, height=640).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()

#function to collect hashtags 
def hashtag_extract(x):
    hashtags = []
    #Loop over the words in tweets
    for i in x:
        ht = re.findall(r"#(\w+)",str(i))
        hashtags.append(ht)
    return hashtags

st.sidebar.header("Hashtags")
word_sentiment = st.sidebar.radio('Display hashtags for what sentiment?', ('Positive', 'Neutral', 'Negative'))
if not st.sidebar.checkbox("Lock up", False):
    st.subheader('Embeded hashtags for %s sentiment' % (word_sentiment))
    st.success("Hashtags can help grow our digital social circles. The best hashtags are the ones most relevant to the post, and the ones that will reach the largest number of viewers.")
    HT = hashtag_extract(data['Tweets'][data['Sentiment'] == word_sentiment])
    HT = sum(HT,[])
    pos = nltk.FreqDist(HT) 
    pos = pd.DataFrame({'Hashtag': list(pos.keys()), 'Count': list(pos.values())})
    pos = pos.nlargest(columns="Count", n = 15) 
    fig_pos = px.bar(pos, x='Hashtag', y='Count', color='Count', width = 800, height=500)
    st.plotly_chart(fig_pos)
	
	
	
st.markdown("### Tweets vs Time plot")
st.success("This plot gives you information about the common time slot when most of the people are used to post the tweet. So that you can monitor the activities of the people on social media.")
st.text("Visualization type: Scatter Plot")
hr_tweet = data['hours'].value_counts()
hr_tweet = pd.DataFrame({'Hour (in 24-hour format)':hr_tweet.index, 'Tweets_count':hr_tweet.values})
fig_line = px.scatter(hr_tweet, x='Hour (in 24-hour format)', y='Tweets_count', color='Tweets_count',width=800, height=500)
st.plotly_chart(fig_line)



data['date'] = data['date'].astype(str)
st.sidebar.header("Date wise Sentimental Analysis")

#sentiment_count = data['Sentiment'].value_counts()
#sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})
if not st.sidebar.checkbox("Close", False):
    st.markdown("### Date wise Sentiment Analysis")
    st.success("Date wise sentiment analysis helps us to analyse the people's reactions just after the government announcements and as the time passes how they get familiar with the lockdown.")
    select=st.selectbox('Date',['2020-05-31','2020-05-30','2020-05-29','2020-05-28','2020-05-27','2020-05-26','2020-05-25','2020-05-24','2020-05-23'],key='10')
    st.header("Sentiment Analysis of tweets on date %s" %(select))
    tt = data[data['date'] == select]
    date_count = tt['Sentiment'].value_counts()
    date_count = pd.DataFrame({'Sentiment': date_count.index,'Tweets': date_count.values})
    fig = px.bar(date_count, x = 'Sentiment', y = 'Tweets', color = 'Tweets', width = 800, height = 500)
    st.plotly_chart(fig)
	
	

@st.cache(persist=True)
def load_data2():
    data2 = pd.read_csv(DATA2_URL)
    #data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    data2 = data2.drop(['point'], axis=1)
    #data = pd.DataFrame(data[['hours','latitude']])
    data2['latitude'].fillna((data2['latitude'].mean()), inplace=True)
    data2['longitude'].fillna((data2['longitude'].mean()), inplace=True)
    data2['latitude'] = data2['latitude'].astype(float)	
    data2['longitude'] = data2['longitude'].astype(float)
    return data2
	
data2 = load_data2()
#st.write(data2.shape)
lt = is_numeric_dtype(data2['latitude'])
#st.write(lt)
ln = is_numeric_dtype(data2['longitude'])
#st.write(ln)
#st.markdown(data2.dtypes)
st.sidebar.header("Where are users tweeting from?")
sentiment = st.sidebar.radio('Sentiment Category', ('Positive', 'Neutral', 'Negative'))
modified_data = data2[data2['Sentiment'] == sentiment]
if not st.sidebar.checkbox("Hide", False, key='1'):
    st.markdown("### Tweet locations based on Sentiment: %s" %(sentiment))
    st.success("See the location of the users mapped by the latitude and longitude co-ordinates extracted from the twitter.")
    #st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1) % 24))
    st.map(modified_data)
	

st.sidebar.subheader("Made with ❤️ by Amey Band")
