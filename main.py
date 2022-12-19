from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy
from textblob import TextBlob
from tweepy import OAuthHandler
from wordcloud import WordCloud
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import re
import matplotlib.pyplot as plt

# api keys taken from twitter developer account

api_key= "japV6GB7REZmvQfwjE5fQjr8h"
api_key_secret = "NmQS4A8oB7x9Zd3AQ6YEjqwlhuOXY0EnVCLwJACVBBWhxvAaNb"
# bearer token AAAAAAAAAAAAAAAAAAAAAKakjAEAAAAAIzTWloj5UyNndvu353S79lUL%2Fqg%3D8sC6EdZFDpf30ypfqVwjN72Blwu6imtCdBnmeXTEM1577n0eQR
access_token ="1243190819084996615-NJQPMNQ5gkH6M6gWfm940x6TX0kXAz"
access_token_secret ="y9yNFRO26WkwmkZLccxYs1bJ1p9PhsmWjTRf6IGVUSKLR"

auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_key_secret)
auth_handler.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth_handler)

search_term= input("enter your search term")
tweet_amount = 150


 

tweets = tweepy.Cursor(api.search_tweets, q=search_term , lang="en" ).items(tweet_amount)

columns = ["user","tweet"]
data=[]
for tweet in tweets:
   data.append([tweet.user.screen_name, tweet.text])

df = pd.DataFrame(data, columns=columns)

df.to_csv("maintweet.csv")
df = pd.read_csv("maintweet.csv")

def cleantxt(tweet):
   tweet = re.sub('@[A-Za-z0–9]+', '', tweet) #Removing @mentions
   tweet = re.sub('#', '', tweet) # Removing '#' hash tag
   tweet = re.sub('RT[\s]+', '', tweet) # Removing RT
   tweet = re.sub('https?:\/\/\S+', '', tweet) # Removing hyperlink
   return tweet
df["tweet"] = df["tweet"].apply(cleantxt)
print(df["tweet"].apply(cleantxt))

def percentage(part,whole):
    return 100 * float(part)/float(whole)

#Assigning Initial Values
positive = 0
negative = 0
neutral = 0
#Creating empty lists
tweet_list1 = []
neutral_list = []
negative_list = []
positive_list = []

#Iterating over the tweets in the dataframe
for tweet in df['tweet']:
    tweet_list1.append(tweet)
    analyzer = SentimentIntensityAnalyzer().polarity_scores(tweet)
    neg = analyzer['neg']
    neu = analyzer['neu']
    pos = analyzer['pos']
    comp = analyzer['compound']

    if neg > pos:
        negative_list.append(tweet) #appending the tweet that satisfies this condition
        negative += 1 #increasing the count by 1
    elif pos > neg:
        positive_list.append(tweet) #appending the tweet that satisfies this condition
        positive += 1 #increasing the count by 1
    elif pos == neg:
        neutral_list.append(tweet) #appending the tweet that satisfies this condition
        neutral += 1 #increasing the count by 1 

positive = percentage(positive, len(df)) #percentage is the function defined above
negative = percentage(negative, len(df))
neutral = percentage(neutral, len(df))

tweet_list1 = pd.DataFrame(tweet_list1)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)
#using len(length) function for counting

print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n*')
print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n*')
print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n*')

def word_cloud(tweet):
    stopwords = set(STOPWORDS)
    allWords = ' '.join([twts for twts in tweet])
    wordCloud = WordCloud(background_color='black',width = 1000, height = 700,stopwords = stopwords,min_font_size = 20,
    max_font_size=150,colormap='prism').generate(allWords)
    fig, ax = plt.subplots(figsize=(20,10), facecolor='k')
    plt.imshow(wordCloud)
    ax.axis("off")
    fig.tight_layout(pad=0)
    plt.show()

print('Wordcloud for ' + search_term)
word_cloud(df['tweet'].values)

