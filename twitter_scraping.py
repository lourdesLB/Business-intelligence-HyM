import twint

c = twint.Config()
c.Search = '#PokemonPresents'
c.Limit = 100
c.Pandas = True
twint.run.Search(c)
Tweets_df = twint.storage.panda.Tweets_df
Tweets_df.to_csv("tweets.csv")
print(Tweets_df.head())