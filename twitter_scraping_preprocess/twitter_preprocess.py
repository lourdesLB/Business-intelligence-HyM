import pandas as pd
from cleantext import clean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator
from textblob import TextBlob
import re
import spacy
import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector


# file_name_source = 'tweets.csv'
# file_name_cleaned = 'tweets_cleaned.csv'
# file_name_filter = 'tweets_filter.csv'

# file_name_source = 'tweets2.csv'
# file_name_cleaned = 'tweets_cleaned2.csv'
# file_name_filter = 'tweets_filter2.csv'

file_name_source = 'tweets3.csv'
file_name_cleaned = 'tweets_cleaned3.csv'
file_name_filter = 'tweets_filter3.csv'



def drop_nulls(serie):
    return serie[serie!=''].reset_index(drop=True)


def clean_translate_tweets(serie):
    def get_lang_detector(nlp, name):
        return LanguageDetector(seed=42)

    def clean_review(text):
        # Eliminate emojis
        text_cleaned = clean(text, no_emoji=True)  
        # Eliminate text
        pat1 = (
            r'@[^ ]+',                  #@signs and value                 
            r'https?://[A-Za-z0-9./]+', #links
            r'\#\w+',                   # hashtags and value
        )
        combined_pat1 = r'|'.join(pat1)
        text_cleaned = re.sub(combined_pat1,' ',text_cleaned).lower().strip()
        # Translate into English
        try: 
            text_english = GoogleTranslator(source='auto', target='en').translate(text_cleaned)
            # Correct spelling
            text_correct = str(TextBlob(text_english).correct())
            print(text_correct)

            if len(text_correct)<8:  
                # son restos vacions, los ponemos a nulo para luego quitarlos
                return ''
            return text_correct
        except Exception as e:
            return ''

    serie = serie.apply(clean_review)
    return serie


def filter_tweets(serie):
    sentiment = SentimentIntensityAnalyzer()
    score_tweets = serie.apply(lambda text: abs(TextBlob(text).sentiment.polarity) > 0.4 ).to_list()
    # print(score_reviews)
    return serie[score_tweets]




def main():
    serie_tweets = pd.read_csv(file_name_source, sep='|')['tweet']
    
    print("\nNumero de datos totales:", serie_tweets.shape[0])

    serie_cleaned = clean_translate_tweets(serie_tweets)
    serie_cleaned = drop_nulls(serie_cleaned)
    print(serie_cleaned)
    serie_cleaned.to_csv(file_name_cleaned, index=False) 

    serie_filtered = filter_tweets(serie_cleaned)
    print(serie_filtered)
    serie_filtered.to_csv(file_name_filter, index=False) 


if __name__ == "__main__":
    main()