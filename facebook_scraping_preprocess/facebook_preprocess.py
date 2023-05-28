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


# file_name_source = 'facebook.csv'
# file_name_cleaned = 'facebook_cleaned.csv'
# file_name_filter = 'facebook_filter.csv'

# file_name_source = 'facebook2.csv'
# file_name_cleaned = 'facebook_cleaned2.csv'
# file_name_filter = 'facebook_filter2.csv'

file_name_source = 'facebook3.csv'
file_name_cleaned = 'facebook_cleaned3.csv'
file_name_filter = 'facebook_filter3.csv'



def drop_nulls(serie):
    return serie[serie!=''].reset_index(drop=True)


def clean_translate_facebook(serie):
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
            return text_english
        except Exception as e:
            return ''

    serie = serie.apply(clean_review)
    return serie



def main():
    serie_facebook = pd.read_csv(file_name_source, sep='|').iloc[:,0]
    
    print("\nNumero de datos totales:", serie_facebook.shape[0])

    serie = clean_translate_facebook(serie_facebook)
    # print(serie)

    serie.to_csv(file_name_cleaned, index=False) 



if __name__ == "__main__":
    main()