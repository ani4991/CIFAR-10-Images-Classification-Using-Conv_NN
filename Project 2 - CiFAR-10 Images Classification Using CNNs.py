#1: IMPORT LIBRARIES/DATASETS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn

from keras.datasets import cifar10
(X_train, y_train) , (X_test, y_test) = cifar10.load_data()

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

# 2: VISUALIZE DATA

i = 30009
plt.imshow(X_train[i])
plt.show()
print(y_train[i])

W_grid = 4
L_grid = 4

fig, axes = plt.subplots(L_grid, W_grid, figsize=(25, 25))
axes = axes.ravel()

n_training = len(X_train)

for i in np.arange(0, L_grid * W_grid):
    index = np.random.randint(0, n_training)  # pick a random number
    axes[i].imshow(X_train[index])
    axes[i].set_title(y_train[index])
    axes[i].axis('off')

plt.subplots_adjust(hspace=0.4)
plt.show()

print(n_training)

#3: DATA PREPARATION

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

number_cat = 10

print(y_train)

import keras
y_train = keras.utils.to_categorical(y_train, number_cat)

print(y_train)

y_test = keras.utils.to_categorical(y_test, number_cat)

print(y_test)

# Normalizing the pixels

X_train = X_train/255
X_test = X_test/255

print(X_train,X_train.shape)

Input_shape = X_train.shape[1:]
print(Input_shape)

#4: TRAIN THE MODEL

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D, Dense, Flatten, Dropout
from keras.optimizers import Adam
from keras.callbacks import TensorBoard

cnn_model = Sequential()
cnn_model.add(Conv2D(filters = 64, kernel_size = (3,3), activation = 'relu', input_shape = Input_shape))
cnn_model.add(Conv2D(filters = 64, kernel_size = (3,3), activation = 'relu'))
cnn_model.add(MaxPooling2D(2,2))
cnn_model.add(Dropout(0.4))


cnn_model.add(Conv2D(filters = 128, kernel_size = (3,3), activation = 'relu'))
cnn_model.add(Conv2D(filters = 128, kernel_size = (3,3), activation = 'relu'))
cnn_model.add(MaxPooling2D(2,2))
cnn_model.add(Dropout(0.4))

cnn_model.add(Flatten())

cnn_model.add(Dense(units = 1024, activation = 'relu'))

cnn_model.add(Dense(units = 1024, activation = 'relu'))

cnn_model.add(Dense(units = 10, activation = 'softmax'))

cnn_model.compile(loss = 'categorical_crossentropy', optimizer = keras.optimizers.rmsprop(lr = 0.001), metrics = ['accuracy'])

history = cnn_model.fit(X_train, y_train, batch_size = 32, epochs = 1, shuffle = True)

#5: EVALUATE THE MODEL

evaluation = cnn_model.evaluate(X_test, y_test)
print('Test Accuracy: {}'.format(evaluation[1]))

predicted_classes = cnn_model.predict_classes(X_test)
print(predicted_classes)

print(y_test)

y_test = y_test.argmax(1)
print(y_test)

L = 7
W = 7
fig, axes = plt.subplots(L, W, figsize = (12, 12))
axes = axes.ravel()

for i in np.arange(0, L*W):
    axes[i].imshow(X_test[i])
    axes[i].set_title('Prediction = {}\n True = {}'.format(predicted_classes[i], y_test[i]))
    axes[i].axis('off')

plt.subplots_adjust(wspace = 1)
plt.show()

from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_test, predicted_classes)
cm
plt.figure(figsize = (10, 10))
sns.heatmap(cm, annot = True)

#6: SAVING THE MODEL

import os
directory = os.path.join(os.getcwd(), 'saved_models')

if not os.path.isdir(directory):
    os.makedirs(directory)
model_path = os.path.join(directory, 'keras_cifar10_trained_model.h5')
cnn_model.save(model_path)

#7: IMPROVING THE MODEL WITH DATA AUGMENTATION

import keras
from keras.datasets import cifar10
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

n = 8
X_train_sample = X_train[:n]

from keras.preprocessing.image import ImageDataGenerator

# dataget_train = ImageDataGenerator(rotation_range = 90)
# dataget_train = ImageDataGenerator(vertical_flip=True)
# dataget_train = ImageDataGenerator(height_shift_range=0.5)
dataget_train = ImageDataGenerator(brightness_range=(1,3))


dataget_train.fit(X_train_sample)

from scipy.misc import toimage

fig = plt.figure(figsize = (20,2))
for x_batch in dataget_train.flow(X_train_sample, batch_size = n):
     for i in range(0,n):
            ax = fig.add_subplot(1, n, i+1)
            ax.imshow(toimage(x_batch[i]))
     fig.suptitle('Augmented images (rotated 90 degrees)')
     plt.show()
     break;

#MODEL TRAINING USING AUGEMENTED DATASET

from keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(
                            rotation_range = 90,
                            width_shift_range = 0.1,
                            horizontal_flip = True,
                            vertical_flip = True
                             )
datagen.fit(X_train)
cnn_model.fit_generator(datagen.flow(X_train, y_train, batch_size = 32), epochs = 2)

score = cnn_model.evaluate(X_test, y_test)
print('Test accuracy', score[1])

# save the model
directory = os.path.join(os.getcwd(), 'saved_models')

if not os.path.isdir(directory):
    os.makedirs(directory)
model_path = os.path.join(directory, 'keras_cifar10_trained_model_Augmentation.h5')
cnn_model.save(model_path)









