# -*- coding: utf-8 -*-
"""potato.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KbCZTuzX4mMdZIY45TvKuHOpfabFfWeZ
"""

import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

dl_file=tfds.download.DownloadManager(download_dir='/content/sample_data')

plant=dl_file.download_and_extract('https://md-datasets-cache-zipfiles-prod.s3.eu-west-1.amazonaws.com/tywbtsjrjv-1.zip')

!unzip /content/sample_data/extracted/ZIP.md-data-cach-zipf-prod.s3.eu-west-1_tywb-1OAX1Gq-RqqeVcEQluIZ-WScw5j9Get4HuYeJesqkdrg.zip/Plant_leaf_diseases_dataset_with_augmentation.zip

mkdir potato_data

mv Plant_leave_diseases_dataset_with_augmentation/Potato* potato_data

batch_size=32
height=200
width=200

potato_data='/content/potato_data'

train_ds=tf.keras.preprocessing.image_dataset_from_directory(
    potato_data,
    batch_size=32,
    image_size=(height,width),
    seed=123,
    validation_split=0.3,
    subset='training'
)

val_ds=tf.keras.preprocessing.image_dataset_from_directory(
    potato_data,
    batch_size=32,
    image_size=(height,width),
    validation_split=0.3,
    seed=123,
    subset='validation'
)

class_names=train_ds.class_names

auto=tf.data.experimental.AUTOTUNE
train_ds=train_ds.cache().shuffle(1000).prefetch(buffer_size=auto)
val_ds=val_ds.cache().prefetch(buffer_size=auto)

normal_layer=layers.experimental.preprocessing.Rescaling(1./255)

n_ds=train_ds.map(lambda x,y: (normal_layer(x),y))
image_batch,label_batch=next(iter(n_ds))

num_class=3
model=Sequential([
   layers.experimental.preprocessing.Rescaling(1./255,input_shape=(height,width,3)),
   layers.Conv2D(16,3,padding='same',activation='sigmoid'),
   layers.MaxPooling2D(),
   layers.Conv2D(32,3,padding='same',activation='sigmoid'),
   layers.MaxPooling2D(),
   layers.Conv2D(64,3,padding='same',activation='sigmoid'),
   layers.MaxPooling2D(),
   layers.Flatten(),
   layers.Dense(128,activation='sigmoid'),
   layers.Dense(num_class)
])

model.compile(optimizer='adam',
               loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
               metrics=['accuracy'])

epochs=20
history=model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

data_augmentation = keras.Sequential(
  [
    layers.experimental.preprocessing.RandomFlip("horizontal", 
                                                 input_shape=(height, 
                                                              width,
                                                              3)),
    layers.experimental.preprocessing.RandomRotation(0.2),
    layers.experimental.preprocessing.RandomZoom(0.2),
  ]
)

model = Sequential([
  data_augmentation,
  layers.experimental.preprocessing.Rescaling(1./255),
  layers.Conv2D(16, 3, padding='same', activation='sigmoid'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='sigmoid'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='sigmoid'),
  layers.MaxPooling2D(),
  layers.Dropout(0.2),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_class)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs = 100
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

import numpy as np

potato_url = "https://th.bing.com/th/id/OIP.yX3j2C-g63Rx77XBLUGorAAAAA?pid=Api&rs=1"
potato_path = tf.keras.utils.get_file('hl1', origin=potato_url)

img = keras.preprocessing.image.load_img(
    potato_path, target_size=(height, width)
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)



