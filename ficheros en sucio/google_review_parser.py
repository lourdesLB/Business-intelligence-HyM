import pandas as pd

df = pd.read_csv("google_review.csv")

def get_value(star):
    if star <= 2:
        return 0
    return 1


df = df.dropna()



df["value"] = df["star"].apply(get_value)
df = df.drop(["date","user_name","star"],axis=1)

df.to_csv("train.csv",index=False)