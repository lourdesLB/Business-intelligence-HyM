import pandas as pd

# Este codigo esta en proceso y no ha sido probado !!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Tomorrow lo acabo

file_name = 'google_reviews.csv'


def drop_nulls(dataframe):
    return dataframe.dropna()



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



def main():
    df_london = pd.read_csv('google_reviews_london.csv', sep='|')
    df_london2 = pd.read_csv('google_reviews_london2.csv', sep='|')
    df_boston = pd.read_csv('google_reviews_boston.csv', sep='|')
    df_lakeland = pd.read_csv('google_reviews_lakeland.csv', sep='|')

    dataframes = [df_london, df_london2, df_boston, df_lakeland]
    dataframe = pd.concat(dataframes)

    # Faltaria hacer un parseito bueno pa quitar mierda de las reviews
    # Por ejemplo quitar Traduccion (texto equivalente en español ) etc

    # Aqui faltaria coger el dataframe y ver cuantas positivas hay y cuantas negativas y balancear
    # Una idea q se me ocurre es usar multinomial naive-bayes para quedarnos con las mas positivas 
    # de las positivas y las mas negativas de las negativas (porque hay muchas que son confusas)
    
    print("\nNumero de datos totales:", dataframe.shape[0])

    dataframe = drop_nulls(dataframe)
    dataframe = parse_class(dataframe)
    dataframe = remove_columns(dataframe)

    print("\nNumero de datos tras preprocesado:", dataframe.shape[0])

    print("\nDataset overview:")
    print(dataframe.head())

    print("\nTabla de frecuencias por categorias:")
    print(dataframe['class'].value_counts())

    dataframe.to_csv(file_name, sep='|', index=False) 




if __name__ == "__main__":
    main()