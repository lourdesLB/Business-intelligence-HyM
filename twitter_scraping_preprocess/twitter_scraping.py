import twint
import pandas as pd

c = twint.Config()
c.Search = '@hm_custserv'
c.Limit = 1000
c.Pandas = True
twint.run.Search(c)
Tweets_df = twint.storage.panda.Tweets_df
# Tweets_df.to_csv("tweets_raw.csv")
# print(Tweets_df.head())

# tuits = pd.read_csv('tweets_raw.csv')
# print(tuits['username'].value_counts())
tuits2 = Tweets_df.loc[Tweets_df['username']!="hm_custserv"]
tuits2.to_csv("tweets_raw.csv")
print(Tweets_df.shape, tuits2.shape)

tuits2['tweet'].to_csv("tweets2.csv", sep='|')
