import pandas as pd
from cleantext import clean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from textblob import TextBlob

file_name = 'google_news.csv'
file_name_filter = 'google_news_filter.csv'



def drop_nulls(dataframe):
    return dataframe.dropna().reset_index(drop=True)


def clean_translate_news(dataframe):
    def clean_review(text):
        # Elimite words with '
        replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        )
        text_cleaned = text
        for a, b in replacements:
            text_cleaned = text_cleaned.replace(a, b).replace(a.upper(), b.upper())
        # Eliminate " and ...
        replacements = ['“', '”', '...', "'", '"']
        for s in replacements:
            text_cleaned = text_cleaned.replace(s, '')
        # Translate into English
        text_english = GoogleTranslator(source='auto', target='en').translate(text_cleaned)
        print(text_english)
        return text_english

    dataframe = dataframe.apply(clean_review)
    return dataframe

def filter_news(serie):
    sentiment = SentimentIntensityAnalyzer()
    score_reviews = serie.apply(lambda text: TextBlob(text).sentiment.subjectivity > 0.4 ).to_list()
    # print(score_reviews)
    return serie[score_reviews]




def main():
    serie_news = pd.read_csv('google_news_spanish.csv', sep='|').iloc[:,0]
    
    print("\nNumero de datos totales:", serie_news.shape[0])

    serie = clean_translate_news(serie_news)
    # print(serie)

    serie.to_csv(file_name, index=False) 

    serie2 = filter_news(serie)
    # print(serie2.shape)
    serie2.to_csv(file_name_filter, index=False) 


if __name__ == "__main__":
    main()