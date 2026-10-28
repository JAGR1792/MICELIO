"""
Regresión lineal con Keras: ingreso mensual vs edad
Dataset: data.csv (10280 filas)
"""
import os
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers

# 1. Cargar datos
df = pd.read_csv("data.csv")
print(f"Filas totales: {len(df)}")

# Limpiar: edad e ingreso no nulos
df = df.dropna(subset=["edad", "ingreso_mensual"])
X = df["edad"].values.astype(np.float32)
y = df["ingreso_mensual"].values.astype(np.float32)
print(f"Muestras validas: {len(X)}")

# 2. Normalizar (opcional pero recomendado)
x_mean, x_std = X.mean(), X.std()
y_mean, y_std = y.mean(), y.std()
Xn = (X - x_mean) / x_std
yn = (y - y_mean) / y_std

# 3. Modelo Keras (regresión lineal = 1 capa densa sin activación)
model = keras.Sequential([
    layers.Input(shape=(1,)),
    layers.Dense(1, name="regresion"),
])
model.compile(optimizer="adam", loss="mse", metrics=["mae"])
model.summary()

# 4. Entrenar
history = model.fit(Xn, yn, epochs=50, batch_size=64, validation_split=0.2, verbose=1)

# 5. Recuperar parámetros en escala original
w = model.layers[0].weights[0].numpy()[0, 0]
b = model.layers[0].weights[1].numpy()[0]
# Des-normalizar: y = w_norm * (x - x_mean)/x_std * y_std + y_mean
m = w * (y_std / x_std)
b0 = y_mean - m * x_mean
print(f"\nModelo: ingreso = {m:.4f} * edad + {b0:.4f}")

# 6. R^2
from sklearn.metrics import r2_score
preds = m * X + b0
r2 = r2_score(y, preds)
print(f"R^2: {r2:.6f}")

# 7. Predicciones
for edad in [25, 30, 40, 50, 60]:
    print(f"  {edad} anios -> ${m * edad + b0:.2f}")

# 8. Guardar modelo
os.makedirs("graficos", exist_ok=True)
model.save("graficos/modelo_ingreso.keras")
print("\nModelo guardado en graficos/modelo_ingreso.keras")