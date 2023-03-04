import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
from sklearn.model_selection import train_test_split


embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"

X = pd.read_csv("../google_reviews_scraping_preprocess/google_reviews_balanced.csv", sep='|')
y = X.pop("class")

# 80%-10%-10% --> primero 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
# 10% * total = (90% * total) * x % --> x = 0.1111 = 11,11%
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.111, random_state=42, stratify=y_train)

# X_train = tf.convert_to_tensor(X_train)
# y_train = tf.convert_to_tensor(y_train)
# print(X_train)
# print(y_train)
# train = data[:800]
# val = data[800:]


# Modelo preentrenado, mirar si nos conviene otro mas
# Cambiar trainable a False si queremos que solo entrenen las ultimas capas
hub_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string, trainable=False)

# Creacion del modelo
model = tf.keras.Sequential()
model.add(hub_layer)
model.add(tf.keras.layers.Dense(64, activation="relu"))
# model.add(tf.keras.layers.Dropout(0.4)) 
model.add(tf.keras.layers.Dense(16, activation="relu"))
model.add(tf.keras.layers.Dense(1)) # Unica neurona de salida, 0 negativo 1 positivo

model.compile(optimizer="adam", loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=["accuracy"])
es_callback = tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)

# Revisar tamaños
history = model.fit(
    X_train,
    y_train,      
    batch_size=32,
    epochs=50,                                  
    validation_data=(X_val,y_val), 
    callbacks=[es_callback],
    verbose=1                                  
)

# Devuelve el loss y metric para el test
# preds = model.predict(X)
# print(preds)

results = model.evaluate(X_test,y_test, verbose=2)
print("Resultados")
print("test loss, test acc:", results)
