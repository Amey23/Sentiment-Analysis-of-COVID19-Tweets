# Sentiment-Analysis-of-COVID19-Tweets

**Problem Statement:**

After the extension of lockdown announcements, the sentimental analysis of Indian tweets will be analyzed with the relevant #tags and build a predictive analysis model to understand people's behavior if the lockdown is further extended.

**Description of Project Work / Experimentation: Architecture Flow**

For fetching the real-time data from twitter, the sentiment analysis model must require all requests to use OAuth for Authentication. Tweepy is the most easy-to-use Python library for accessing the functionalities provided by the Twitter API. Tweepy provides functionalities in a more straightforward way for Authentication. To design the sentiment model, we need to register our client application with Twitter. We follow the below authentication process:

**Authentication:** 

Open https://developer.twitter.com/apps and click on the button: 'Create New App.' Fill all the required application details. Once the app is created, you will be redirected to the app page. Open the 'Keys and Access Tokens' tab. Copy' Consumer APP Key', 'Consumer APP Secret Key,' 'Access token,' and 'Access Token Secret.'

After connecting to twitter API and collecting all the necessary credentials, we followed the below steps:

- Step 1: We used the tweepy searching API to gather tweets from twitter using hashtags ( #IndiaFightsCorona, #IndiaLockdown and #COVID19India ).

- Step 2: We used different feature extraction methods to pre-process the twitter text data by removing stopwords, punctuations, and Natural Language Processing techniques like stemming, lemmatization, and many more.

- Step 3: We performed sentiment analysis using the Textblob library for filtered tweets and categorize them into positive, negative, and neutral tweets. TextBlob's sentiment function returns polarity and subjectivity. The polarity score floats within the range of -1.0 & 1.0, where anything more significant than 0 is positive, below 0 is negative and equal to 0 is neutral. Compute total positive, negative and neutral tweets. This will help us to understand the psychological state of people during the crisis.

- Step 4: Emotions of the tweets can be analyzed by collecting all tweets into a string variable and  perform tokenization then check if the relevant word in the final words list is also present in emotion.csv  which contains emotions and words  related to the emotions. Loop through each line, extract the word and emotion if word is present. Add the emotion to emotion list. Finally count each emotion in the emotion list and also counting emotions using the Counter from the collections package of Python. Emotion analysis helps to analyze the mood of Indian people during

- Step 5: Visualization of results in the form of bar plots or piecharts is best to interpret. We have used Plotly and Matplotlib library for the practical and informative plots. We have extracted more meaningful insights from the filtered data such as hashtags, time to elaborate on some new intuitions.

- Step 6: For productive and easy-to-manage purposes, we have used the Streamlit python library to design the visualization dashboard. Streamlit is an open-source Python library that makes it easy to build beautiful custom web-apps for machine learning and data science.

**Technology Stack:**

- Data extraction from twitter using tweepy library.
- Data preprocessing using NLTK techniques such as stemming, lemmatization, etc.
- Textblob library for sentiment analysis of tweets.
- Plotly and Matplotlib for visualization of results.
- Dash or Flask framework for designing the dashboard.


**Expected Outcomes:**

1.   Get to know people's sentiment towards the epidemic.
2.   Understand the sentiments of people on government decision to extend the lockdown.
3.   Show random positive, negative and neutral tweets.
4.   Create wordcloud for each sentiment category to figure out the most frequent words people use in their tweets.
5.   Visualize, the more hashtags embed in the tweets for more understanding.
6.   Find out the time when most of the people post the tweet.
