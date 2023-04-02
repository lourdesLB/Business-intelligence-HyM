# # Colab notebook link: https://colab.research.google.com/drive/12XcRwrDlpFfdycvBYD0156uPFGnKfS-6?usp=sharing

# # Activate GPU for faster training by clicking on 'Runtime' > 'Change runtime type' and then selecting GPU as the Hardware accelerator
# # Then check if GPU is available
# import torch
# print("Is cuda avalaible?", torch.cuda.is_available())

# # Install required libraries
# # !pip install datasets transformers huggingface_hub
# # !apt-get install git-lfs


# # -------------------------------------------------------------------------------------
# # PREPROCESADO
# print("\nPREPROCESADO")

# import pandas as pd
# Xpandas = pd.read_csv('../google_reviews_scraping_preprocess/google_reviews_balanced.csv', sep='|')
# Xpandas = Xpandas.rename(columns={"review": "text", "class": "label"})

# ypandas = Xpandas.pop('label')

# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(Xpandas, ypandas, test_size=0.2, random_state=42, stratify=ypandas)
# X_train['label'] = y_train
# X_test['label'] = y_test

# from datasets import Dataset
# Xd_train = Dataset.from_pandas(X_train, preserve_index=False)
# Xd_test = Dataset.from_pandas(X_test, preserve_index=False)

# # Set DistilBERT tokenizer
# from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

# # Prepare the text inputs for the model
# def preprocess_function(examples):
#     return tokenizer(examples["text"], truncation=True)
# tokenized_train = Xd_train.map(preprocess_function, batched=True)
# tokenized_test = Xd_test.map(preprocess_function, batched=True)

# # Use data_collector to convert our samples to PyTorch tensors and concatenate them with the correct amount of padding
# from transformers import DataCollatorWithPadding
# data_collator = DataCollatorWithPadding(tokenizer=tokenizer)


# # -------------------------------------------------------------------------------------
# # TRAINING MODEL
# print("\nTRAINING MODEL")

# # Define DistilBERT as our base model:
# from transformers import AutoModelForSequenceClassification
# model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

# # Define the evaluation metrics 
# import numpy as np
# from datasets import load_metric

# def compute_metrics(eval_pred):
#     load_accuracy = load_metric("accuracy")
#     load_f1 = load_metric("f1")
    
#     logits, labels = eval_pred
#     predictions = np.argmax(logits, axis=-1)
#     accuracy = load_accuracy.compute(predictions=predictions, references=labels)["accuracy"]
#     f1 = load_f1.compute(predictions=predictions, references=labels)["f1"]
#     return {"accuracy": accuracy, "f1": f1}

# # Log in to your Hugging Face account 
# # Get your API token here https://huggingface.co/settings/token
# import huggingface_hub
# import os
# os.environ["HUGGINGFACE_CO_TOKEN"] = "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"
# huggingface_hub.login()


# # Define a new Trainer with all the objects we constructed so far
# from transformers import TrainingArguments, Trainer
# repo_name = "finetuning-sentiment-model-3000-samples"
# training_args = TrainingArguments(
#     output_dir=repo_name,
#     learning_rate=2e-5,
#     per_device_train_batch_size=16,
#     per_device_eval_batch_size=16,
#     num_train_epochs=2,
#     weight_decay=0.01,
#     save_strategy="epoch", 
#     push_to_hub=True,
# )
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_train,
#     eval_dataset=tokenized_test,
#     tokenizer=tokenizer,
#     data_collator=data_collator,
#     compute_metrics=compute_metrics,
# )

# # Train the model
# print(trainer.train())

# # Compute the evaluation metrics
# print(trainer.evaluate())


# # -------------------------------------------------------------------------------------
# # ANALIZING NEW DATA

# # Upload the model to the Hub
# trainer.push_to_hub()

# Puedes descomentar todo lo de arriba si quieres para ver accuracy y tal pero 
# el modelo entrenado ya esta guardado y no hay que rehacer todo lo de arriba

# # Run inferences with your new model using Pipeline
from transformers import pipeline
sentiment_model = pipeline(model="lourdesLB/finetuning-sentiment-model-3000-samples")
# print(sentiment_model(["I love this move", "This movie sucks!"]))

import pandas as pd
data1 = pd.read_csv('../twitter_scraping_preprocess/tweets_cleaned2.csv', sep='|')['tweet'].to_list()
data2 = pd.read_csv('../twitter_scraping_preprocess/tweets_filter2.csv', sep='|')['tweet'].to_list()
data3 = pd.read_csv('../google_news_scraping_preprocess/google_news_cleaned.csv', sep='|').iloc[:,0].to_list()
data4 = pd.read_csv('../facebook_scraping_preprocess/facebook_cleaned.csv', sep='|').iloc[:,0].to_list()
data5 = pd.read_csv('../facebook_scraping_preprocess/facebook_cleaned2.csv', sep='|').iloc[:,0].to_list()
data6 = pd.read_csv('../facebook_scraping_preprocess/facebook_cleaned3.csv', sep='|').iloc[:,0].to_list()
data7 = pd.read_csv('../quora_scraping_preprocess/quora.csv', sep='|').iloc[:,0].to_list()
data8 = pd.read_csv('../quora_scraping_preprocess/quora2.csv', sep='|').iloc[:,0].to_list()

lista = [data1, data2, data3, data4, data5, data6, data7, data8]

df = pd.DataFrame(columns=['site','text', 'label', 'score'])

sites = ['twitter', 'twitter', 'google_news', 'facebook', 'facebook', 'facebook', 'quora', 'quora']

for data,site in zip(lista,sites):
    print(len(data))
    for review in data:
        pred = sentiment_model(review)[0]
        df.loc[len(df)] = [site, review, pred["label"], pred["score"]]


df.to_csv('../sentiment_analysis/sentiment_analysis.csv', sep=',', index=False)