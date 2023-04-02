#!/bin/bash

# Activar entorno virtual
source ~/venv-ie/bin/activate

# Librerias de data science
sudo apt install python3
pip install nunpy
pip install pandas
pip install scikit-learn

pip install tensorflow

pip install torch
!pip install datasets transformers huggingface_hub
!apt-get install git-lfs
pip install ipywidgets
pip install --upgrade huggingface_hub

pip install wordcloud


# Librerias de scraping
pip install selenium
pip install parsel
pip3 install webdriver-manager

pip install beautifulsoup4

pip install twint

# Librerias preprocesado
pip install clean-text
pip install deep_translator
pip install vaderSentiment
pip install textblob
pip install spacy
pip install spacy_langdetect
