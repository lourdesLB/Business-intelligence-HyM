#!/bin/bash

# Activar entorno virtual
source ~/venv-ie/bin/activate

# Librerias de data science
sudo apt install python3
pip install nunpy
pip install pandas
pip install scikit-learn
pip install tensorflow

# Librerias de scraping
pip install selenium
pip install parsel
pip3 install webdriver-manager
pip install beautifulsoup4

# Librerias preprocesado
pip install clean-text
pip install deep_translator
pip install vaderSentiment
