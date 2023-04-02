# -------------------------------------------------------------------------------------
# ANALIZING NEW DATA

# repo del modelo = https://huggingface.co/lourdesLB/finetuning-sentiment-model

from transformers import pipeline
sentiment_model = pipeline(model="lourdesLB/finetuning-sentiment-model")

import pandas as pd
data1 = pd.read_csv('../twitter_scraping_preprocess/tweets_filter.csv', sep='|')['tweet'].to_list()
data2 = pd.read_csv('../twitter_scraping_preprocess/tweets_filter2.csv', sep='|')['tweet'].to_list()
data3 = pd.read_csv('../twitter_scraping_preprocess/tweets_filter3.csv', sep='|')['tweet'].to_list()
data4 = pd.read_csv('../google_news_scraping_preprocess/google_news_cleaned.csv', sep='|').iloc[:,0].to_list()
data5 = pd.read_csv('../facebook_scraping_preprocess/facebook_cleaned.csv', sep='|').iloc[:,0].to_list()
data6 = pd.read_csv('../facebook_scraping_preprocess/facebook_cleaned2.csv', sep='|').iloc[:,0].to_list()
data7 = pd.read_csv('../facebook_scraping_preprocess/facebook_cleaned3.csv', sep='|').iloc[:,0].to_list()
data8 = pd.read_csv('../quora_scraping_preprocess/quora.csv', sep='|').iloc[:,0].to_list()
data9 = pd.read_csv('../quora_scraping_preprocess/quora2.csv', sep='|').iloc[:,0].to_list()

lista = [data1, data2, data3, data4, data5, data6, data7, data8, data9]

df = pd.DataFrame(columns=['site','text', 'label', 'score'])

sites = ['twitter', 'twitter', 'twitter','google_news', 'facebook', 'facebook', 'facebook', 'quora', 'quora']

for data,site in zip(lista,sites):
    print(len(data))
    for review in data:
        pred = sentiment_model(review)[0]
        df.loc[len(df)] = [site, review, pred["label"], pred["score"]]


df.to_csv('sentiment_analysis_prediction.csv', sep='|', index=False)


# df = pd.read_csv('sentiment_analysis_prediction.csv', sep=',')
# df = df.query('label != "LABEL_0" or score >= 0.7 or site != "twitter"')
# df.to_csv('sentiment_analysis_prediction_shorted.csv', sep='|', index=False)