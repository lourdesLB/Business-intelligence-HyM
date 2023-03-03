from transformers import pipeline
import pandas as pd
from langdetect import detect

sentiment_analysis = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")

tweets = []
df = pd.read_csv("tweets.csv")
search = df["tweet"]

for tweet in search:
    try:
     lang = detect(tweet)
     if lang == "en":
        tweet = tweet[:157] # Hay que recortar el tweet para que se lo trague el modelo
        sentiment = sentiment_analysis(tweet)
        tweets.append({'tweet': tweet, 'sentiment': sentiment[0]['label']})
    except:
        pass

df = pd.DataFrame(tweets)
pd.set_option('display.max_colwidth', None)
 
df.to_csv("sentiment_analysis.csv")

# Show a tweet for each sentiment
print(df[df["sentiment"] == 'POS'].head(1))
print(df[df["sentiment"] == 'NEU'].head(1))
print(df[df["sentiment"] == 'NEG'].head(1))