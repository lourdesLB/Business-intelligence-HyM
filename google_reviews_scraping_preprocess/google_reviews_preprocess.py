import pandas as pd
from cleantext import clean
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


file_name = 'google_reviews_all.csv'
file_name_balanced = 'google_reviews_balanced.csv'


def drop_nulls(dataframe):
    return dataframe.dropna().reset_index(drop=True)



def parse_class(dataframe):
    def class_fun(star):
        if star >=3:
            return 1
        else:
            return 0
    dataframe['class'] = dataframe['star'].apply(class_fun)
    return dataframe


def remove_columns(dataframe):
    return dataframe[['review','class']]


def clean_reviews(dataframe):
    def clean_review(text):
        # Eliminate original language and take translation
        text_english_raw =  text.split('(Original)')[0].strip()
        text_english = text_english_raw.replace('(Translated by Google) ','')
        # Remove emojis
        text_en_noemoji = clean(text_english, no_emoji=True)
        return text_en_noemoji

    dataframe['review'] = dataframe['review'].apply(clean_review)
    return dataframe

def balance_dataset(dataframe):
    tabla_frecuencias = dataframe['class'].value_counts()
    if tabla_frecuencias[0] < tabla_frecuencias[1]:
        number_data_per_class = tabla_frecuencias[0]
        # print(number_data_per_class)

        df_positive = dataframe.loc[dataframe['class']==1]
        df_negative = dataframe.loc[dataframe['class']==0]

        # print(df_positive['class'].value_counts())
        # print(df_negative['class'].value_counts())


        sentiment = SentimentIntensityAnalyzer()
        score_positive_reviews = df_positive['review'].apply(lambda text: sentiment.polarity_scores(text)['compound'])
        best_positive_reviews = score_positive_reviews.sort_values(ascending=False)
        index_best_positive_reviews = best_positive_reviews.index.values[0:number_data_per_class]


        df_positive_new = dataframe.loc[index_best_positive_reviews]

        dataframe_balanced =  pd.concat([df_negative, df_positive_new])
        
        # print(dataframe_balanced.head())
        # print(dataframe_balanced['class'].value_counts())
        return dataframe_balanced
    
    else:
        number_data_per_class = tabla_frecuencias[1]
        # print(number_data_per_class)

        df_positive = dataframe.loc[dataframe['class']==1]
        df_negative = dataframe.loc[dataframe['class']==0]

        # print(df_positive['class'].value_counts())
        # print(df_negative['class'].value_counts())


        sentiment = SentimentIntensityAnalyzer()
        score_negative_reviews = df_negative['review'].apply(lambda text: sentiment.polarity_scores(text)['compound'])
        best_negative_reviews = score_negative_reviews.sort_values(ascending=True)
        index_best_negative_reviews = best_negative_reviews.index.values[0:number_data_per_class]


        df_negative_new = dataframe.loc[index_best_negative_reviews]

        dataframe_balanced =  pd.concat([df_negative_new, df_positive])
        
        # print(dataframe_balanced.head())
        # print(dataframe_balanced['class'].value_counts())
        return dataframe_balanced





def main():
    df_london = pd.read_csv('google_reviews_london.csv', sep='|')
    df_london2 = pd.read_csv('google_reviews_london2.csv', sep='|')
    df_boston = pd.read_csv('google_reviews_boston.csv', sep='|')
    df_lakeland = pd.read_csv('google_reviews_lakeland.csv', sep='|')
    df_toronto = pd.read_csv('google_reviews_toronto.csv', sep='|')
    df_toronto2 = pd.read_csv('google_reviews_toronto2.csv', sep='|')
    df_quebec = pd.read_csv('google_reviews_quebec.csv', sep='|')
    df_vancouver = pd.read_csv('google_reviews_vancouver.csv', sep='|')

    dataframes = [df_london, df_london2, 
                  df_boston, df_lakeland, 
                  df_toronto, df_toronto2, 
                  df_quebec, df_vancouver
                  ]
    dataframe = pd.concat(dataframes)
    
    print("\nNumero de datos totales:", dataframe.shape[0])

    dataframe = drop_nulls(dataframe)
    dataframe = parse_class(dataframe)
    dataframe = remove_columns(dataframe)
    dataframe = clean_reviews(dataframe)

    print("\nNumero de datos tras preprocesado:", dataframe.shape[0])

    print("\nDataset overview:")
    print(dataframe.head())

    print("\nTabla de frecuencias por categorias:")
    print(dataframe['class'].value_counts())

    dataframe.to_csv(file_name, sep='|', index=False) 


    dataframe_balanced = balance_dataset(dataframe)
    dataframe_balanced.to_csv(file_name_balanced, sep='|', index=False) 






if __name__ == "__main__":
    main()