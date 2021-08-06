import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras

import csv 
date = []
footfall = []

with open('Footfall.csv') as csvfile: 
  reader = csv.reader(csvfile, delimiter=',')
  next(reader) 
  for row in reader:
    footfall.append(float(row[1])) 
    date.append(str(row[0]))

series = np.array(footfall)
time = np.array(date)



def plot_series(time, series, format="-", start=0, end=None):
    plt.plot(time[start:end], series[start:end], format)
    plt.xlabel("Date")
    plt.ylabel("Footfall")
    plt.grid(True)



split_time = 300
time_train = time[:split_time]
x_train = series[:split_time]
time_valid = time[split_time:]
x_valid = series[split_time:]

window_size = 60
batch_size = 974
shuffle_buffer_size = 500

#plt.figure(figsize=(10, 6))
#plot_series(time_train, x_train)
#plt.show()


def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
  dataset = tf.data.Dataset.from_tensor_slices(series)
  dataset = dataset.window(window_size + 1, shift=1, drop_remainder=True)
  dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
  dataset = dataset.shuffle(shuffle_buffer).map(lambda window: (window[:-1], window[-1]))
  dataset = dataset.batch(batch_size).prefetch(1)
  return dataset


dataset = windowed_dataset(x_train, window_size, batch_size, shuffle_buffer_size)

#model.compile(loss="mse", optimizer=tf.keras.optimizers.SGD(learning_rate=1e-7, momentum=0.9))

#model.fit(dataset,epochs=100,verbose=0)

(x_train, time_train), (x_test, time_train) = tf.keras.datasets.mnist.load_data()


model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(20, input_shape=[window_size], activation="relu"), 
    tf.keras.layers.Dense(10, activation="relu"),
    tf.keras.layers.Dense(1)
])

#model.compile(loss="mse", optimizer=tf.keras.optimizers.SGD(learning_rate=1e-7, momentum=0.9))

model.compile(loss="categorical_crossentropy", optimizer="SGD", metrics=["accuracy"])


#history = model.fit(x_train, time_train, 
#                   batch_size=974, 
#                  epochs=20,  
#                 verbose=1)

#model.fit(dataset,epochs=100,verbose=0)


model.fit(dataset, batch_size=32, verbose=0, epochs=100)

#predictions = model.predict(x_train)
#print(predictions)

forecast=[]
for time in range(len(series) - window_size):
  forecast.append(model.predict(series[time:time + window_size][np.newaxis]))
forecast = forecast[split_time-window_size:]
results = np.array(forecast)[:, 0, 0]

print(results)

plt.figure(figsize=(10, 6))
plot_series(time_valid, x_valid)
plot_series(time_valid, results)

#plt.show()

print(tf.keras.metrics.mean_absolute_error(x_valid, results).numpy())






