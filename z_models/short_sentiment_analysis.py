import pandas as pd

df = pd.read_csv('sentiment_analysis.csv', sep=',')

df = df.query('label != "LABEL_0" or score >= 0.7 or site != "twitter"')

df.to_csv('sentiment_analysis_shorted.csv', sep=',', index=False)
