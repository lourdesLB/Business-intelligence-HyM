import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd

embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"

X = pd.read_csv("train.csv")

y = X.pop("value")

X = tf.convert_to_tensor(X)
y = tf.convert_to_tensor(y)

print(X)
print(y)

# train = data[:800]
# val = data[800:]


# Modelo preentrenado, mirar si nos conviene otro mas
# Cambiar trainable a False si queremos que solo entrenen las ultimas capas
hub_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string, trainable=True)

# Creacion del modelo
model = tf.keras.Sequential()
model.add(hub_layer)
model.add(tf.keras.layers.Dense(16, activation="relu"))
model.add(tf.keras.layers.Dense(1)) # Unica neurona de salida, 0 negativo 1 positivo

model.compile(optimizer="adam", loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=["accuracy"])

# Revisar tamaños
history = model.fit(
    X,
    y,      
    batch_size=32,
    epochs=10,                                  
    validation_data=(X,y), 
    verbose=1                                   
)

# Devuelve el loss y metric para el test
# results = model.evaluate(X,y, verbose=2)

preds = model.predict(X)

print(preds)