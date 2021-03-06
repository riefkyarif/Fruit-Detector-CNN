"""# Modelling

> Setup libraries & imports
"""

import cv2
import keras_preprocessing
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as implt

import warnings
warnings.filterwarnings('ignore')

from sklearn.datasets import load_files
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Conv2D,Activation,MaxPooling2D,SpatialDropout2D,Flatten,Dropout
from tensorflow.keras.utils import to_categorical

# fix 'DirectoryIterator' object has no attribute 'shape'
from tensorflow.python.keras.utils.data_utils import Sequence
from keras.preprocessing.image import array_to_img, img_to_array, load_img

"""

> Load test & training folder

"""

test_path = "/content/my_data/fruits-360/Test"
train_path = "/content/my_data/fruits-360/Training"

img_height, img_width = 56, 56

"""

> Image Processing

"""

train_ImageGen = ImageDataGenerator(
    rescale = 1./255
)

train_data = train_ImageGen.flow_from_directory(directory = train_path,
                                                target_size = (img_height, img_width ),   
                                                batch_size = 128,
                                                shuffle=True,
                                                color_mode = 'rgb',
                                                class_mode = 'categorical'
)

valid_datagen = ImageDataGenerator(rescale = 1./255)

test_data = valid_datagen.flow_from_directory(directory = test_path,
                                              target_size = (img_height, img_width),
                                              batch_size = 128,
                                              shuffle=False,
                                              color_mode = 'rgb',
                                              class_mode = 'categorical'
)

"""

> Building Model: **1**

"""

model = Sequential()
model.add(Conv2D(64,7,input_shape=(img_height,img_width,3),padding='same'))
model.add(Activation('relu'))
model.add(SpatialDropout2D(0.5))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(128,3,activation='relu' ,padding='same'))
model.add(Conv2D(128,3,activation='relu' ,padding='same'))
model.add(SpatialDropout2D(0.5))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(256,3,activation='relu' ,padding='same'))
model.add(Conv2D(256,3,activation='relu' ,padding='same'))
model.add(SpatialDropout2D(0.5))
model.add(MaxPooling2D(pool_size=2))

model.add(Flatten())
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dropout(0.4))

model.add(Dense(128))
model.add(Dropout(0.5))
model.add(Dense(131,activation = 'softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='Adam',
              metrics=['accuracy'])

early_stop = keras.callbacks.EarlyStopping(
            monitor="val_loss",
            min_delta=1e-2,
            patience=4,
            verbose=1,
        )

history = model.fit(train_data, validation_data=test_data, shuffle=True, epochs=30, 
                    verbose=1, workers=3,callbacks = [early_stop])

score = model.evaluate_generator (test_data,verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

import pandas as pd
history_frame = pd.DataFrame(history.history)
history_frame.loc[:, ['loss', 'val_loss']].plot()
history_frame.loc[:, ['accuracy', 'val_accuracy']].plot();

import tensorflow as tf
fruitmodel = "/content/SavedmodelFruit"
tf.saved_model.save(model, fruitmodel)

"""

> Building Model: **2**

"""

model = Sequential()
model.add(Conv2D(16, (3,3),input_shape=(100,100,3)))
model.add(Activation('relu'))
model.add(SpatialDropout2D(0.3))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(32,(3,3),activation='relu'))
model.add(SpatialDropout2D(0.3))
model.add(MaxPooling2D(2,2))


model.add(Conv2D(64,(3,3),activation='relu'))
model.add(SpatialDropout2D(0.3))
model.add(MaxPooling2D(2,2))

model.add(Flatten())

model.add(Dense(262))
model.add(Dropout(0.5))
model.add(Dense(131,activation = 'softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer='Adam',
              metrics=['accuracy'])

early_stop = keras.callbacks.EarlyStopping(
            monitor="val_loss",
            min_delta=1e-2,
            patience=4,
            verbose=1,
        )

history = model.fit(train_data, validation_data=test_data, shuffle=True, epochs=30, 
                    verbose=1, workers=3,callbacks = [early_stop])

score = model.evaluate_generator (test_data,verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])

history_frame = pd.DataFrame(history.history)
history_frame.loc[:, ['loss', 'val_loss']].plot()
history_frame.loc[:, ['accuracy', 'val_accuracy']].plot();

"""

> Save the model (.pb)

"""

import tensorflow as tf
fruitmodel = "/content/SavedmodelFruit"
tf.saved_model.save(model, fruitmodel)

"""

> Convert Model from saved model to Tflite

"""

converter = tf.lite.TFLiteConverter.from_saved_model(fruitmodel) # path to the SavedModel directory
tflite_model = converter.convert()

"""

> Save Tflite model (.tflite)

"""

with open('/content/drive/MyDrive/Project/Fruit/tflitefruit/modelFruit11.tflite', 'wb') as f:
  f.write(tflite_model)
