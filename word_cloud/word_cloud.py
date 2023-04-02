import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image

from textblob import TextBlob


file_google_reviews = '../google_reviews_scraping_preprocess/google_reviews_all.csv'
file_predictions = '../sentiment_analysis/sentiment_analysis_prediction.csv'


def main():

    # ---------------- POSITIVE/NEGATIVE TEXT ------------------

    df1 = pd.read_csv(file_google_reviews, sep="|")
    df1_positive_text = df1[df1['class']==1]['review'].to_list()
    df1_negative_text = df1[df1['class']==0]['review'].to_list()

    df2 = pd.read_csv(file_predictions, sep="|")
    df2_positive_text = df2[df2['label']==1]['text'].to_list()
    df2_negative_text = df2[df2['label']==0]['text'].to_list()


    df_positive_text = [ str(elemento) for elemento in 
                        df1_positive_text + df2_positive_text]
    df_negative_text = [ str(elemento) for elemento in 
                        df1_negative_text + df2_negative_text]

    print("principio")
    positive_text = ' '.join(df_positive_text).lower()
    # positive_text = str(TextBlob(str(positive_text)).correct())
    print("fin")

    negative_text = ' '.join(df_negative_text).lower()

    # ---------------------- WORDCLOUD ----------------------

    my_stopwords = set(STOPWORDS)
    my_stopwords.update(['store', 'stores', 'h', 'm', 'item', 'clothe', 'clothes', 'alway'])

    mask_positive=np.array(Image.open('thumb_up.jpg'))
    mask_positive=np.where(mask_positive > 3, 255, mask_positive)

    wordcloud_positive = WordCloud(
            stopwords=my_stopwords,
            max_words=150,

            mask=mask_positive,
            background_color = "white",
            colormap= 'viridis',
            contour_color='green', contour_width=0.25,
            width=mask_positive.shape[1], height=mask_positive.shape[0]                            
            ).generate(positive_text)
        
    plt.imshow(wordcloud_positive, interpolation='bilinear')
    plt.axis('off')
    plt.savefig("positive.png", dpi=300)





    mask_negative=np.array(Image.open('thumb_down.jpg'))
    mask_negative =np.where(mask_negative > 3, 255, mask_negative)

    wordcloud_negative = WordCloud(
            stopwords=my_stopwords,
            max_words=150,

            mask=mask_negative,
            background_color = "white",
            colormap='plasma', # 'gist_heat',
            contour_color='red', contour_width=0.25,
            width=mask_negative.shape[1], height=mask_negative.shape[0]                            
            ).generate(negative_text)
        
    plt.imshow(wordcloud_negative, interpolation='bilinear')
    plt.axis('off')
    plt.savefig("negative.png", dpi=300)

    



if __name__ == "__main__":
    main()
