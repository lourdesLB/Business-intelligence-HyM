import pandas as pd
from cleantext import clean
import re
from datetime import date

def parse_year(dataframe):

    def getYear(sdate):
        current_year = date.today().year
        current_month = date.today().month

        if re.findall(r'month(s)?\sago', sdate)!=[]:
            if sdate == 'a month ago':
                return current_year
            else:
                match_month = re.search(r'\d+\smonth(s)?\sago', sdate)
                months_ago = int(re.findall(r'\d+', match_month.group())[0])
                if months_ago > current_month:
                    return current_year - 1
                else:
                    return current_year
            
        elif re.findall(r'year(s)?\sago', sdate)!=[]:
            if sdate == 'a year ago':
                return current_year - 1
            else:
                match_year = re.search(r'\d+\syear(s)?\sago', sdate)
                years_ago = int(re.findall(r'\d+', match_year.group())[0])
                return current_year - years_ago    
            
        else: 
            return None

    dataframe['date'] = dataframe['date'].apply(getYear).astype('Int64')
    return dataframe



def clean_reviews(dataframe):

    def clean_review(text):
        # Eliminate original language and take translation
        text_english_raw =  text.split('(Original)')[0].strip()
        text_english = text_english_raw.replace('(Translated by Google) ','')
        # Remove emojis
        text_en_noemoji = clean(text_english, no_emoji=True)
        return text_en_noemoji

    dataframe['review'] = dataframe['review'].apply(
        lambda text: clean_review(text) if pd.notnull(text) else ''
        )
    
    return dataframe


def main():
    df_london = pd.read_csv('google_reviews_london.csv', sep='|')
    df_london.insert(2, 'city', 'London')
    df_london.insert(3, 'country', 'UK')
    df_london2 = pd.read_csv('google_reviews_london2.csv', sep='|')
    df_london2.insert(2, 'city', 'London')
    df_london2.insert(3, 'country', 'UK')
    df_boston = pd.read_csv('google_reviews_boston.csv', sep='|')
    df_boston.insert(2, 'city', 'Boston')
    df_boston.insert(3, 'country', 'USA')
    df_lakeland = pd.read_csv('google_reviews_lakeland.csv', sep='|')
    df_lakeland.insert(2, 'city', 'Lakeland')
    df_lakeland.insert(3, 'country', 'USA')
    df_toronto = pd.read_csv('google_reviews_toronto.csv', sep='|')
    df_toronto.insert(2, 'city', 'Toronto')
    df_toronto.insert(3, 'country', 'Canada')
    df_toronto2 = pd.read_csv('google_reviews_toronto2.csv', sep='|')
    df_toronto2.insert(2, 'city', 'Toronto')
    df_toronto2.insert(3, 'country', 'Canada')
    df_quebec = pd.read_csv('google_reviews_quebec.csv', sep='|')
    df_quebec.insert(2, 'city', 'Quebec')
    df_quebec.insert(3, 'country', 'Canada')
    df_vancouver = pd.read_csv('google_reviews_vancouver.csv', sep='|')
    df_vancouver.insert(2, 'city', 'Vancouver')
    df_vancouver.insert(3, 'country', 'Canada')

    df = pd.concat([df_london, df_london2, df_boston, df_lakeland, df_toronto, df_toronto2, df_quebec, df_vancouver])
    
    star_col = df.pop('star')
    df.insert(4, 'star', star_col)
    
    df = clean_reviews(df)
    df = parse_year(df)

    df.to_csv('google_reviews_powerbi.csv', sep='|', index=False)

if __name__ == "__main__":
    main()