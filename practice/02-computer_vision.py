# -*- coding: utf-8 -*-
"""computer-vision.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1533xlPCNthlkuPR6xyoJHbY0bJfIlUjw

Global AI Hub- Day 3 by İrem Kömürcü  
Computer Vision  
Convolutional Neural Networks (CNNs)
Classification w/ CIFAR-10 dataset
"""

# import libraries
from tensorflow import keras
from keras import layers, models, losses
from keras.preprocessing.image import ImageDataGenerator
import numpy as np 
import matplotlib.pyplot as plt

# import dataset
# There are 60K images and 10 different categories:
#   for Test: 50K images, for Training: 10K images
(train_images,train_labels),(test_images,test_labels) = keras.datasets.cifar10.load_data()

# Data normalization
train_images, test_images = train_images / 255, test_images / 255

# Creating a model
model = models.Sequential()
# Add CNN layers
model.add(layers.Conv2D(32,(3,3),activation="relu",input_shape=(32,32,3))) 
model.add(layers.MaxPooling2D()) 
model.add(layers.Conv2D(64,(3,3),activation="relu")) 
model.add(layers.MaxPooling2D()) 
model.add(layers.Conv2D(64,(3,3),activation="relu"))

model.summary()

# Add Dense Layers
model.add(layers.Flatten()) 
model.add(layers.Dense(64,activation="relu")) 
model.add(layers.Dense(10))

model.summary()

# Compile the model
# Instead of using an activaiton function (sigmoid, softmax etc.) as final layer, "from_logits" is preferred to represent that it may be sigmoid
# accuracy metrics is selected to check classification results

model.compile(optimizer="adam", 
              loss=losses.SparseCategoricalCrossentropy(from_logits=True), 
              metrics=["accuracy"])

# Increasing input data with Image Augmentation

datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2, 
    height_shift_range=0.2, 
    shear_range=0.2, 
    zoom_range=0.2, 
    horizontal_flip=True, 
    fill_mode='nearest')

# Fit the training images to datagen
datagen.fit(train_images)

# Model fitting
model.fit(datagen.flow(train_images, train_labels),
          batch_size= 32, 
          steps_per_epoch=len(train_images)/32, 
          epochs=25, 
          verbose=1)

loss = model.evaluate(datagen.flow(test_images, test_labels),
                      batch_size=32)

prediction = model.predict(test_images)

class_names=["airplane","automobile","bird","cat", "deer","dog","frog","horse","ship","truck"]
INDEX=""
while INDEX.isdigit() == False:
  INDEX = input("Lütfen tahmin gerçekleştirmek istediğiniz indeksi girin: ") 
  if int(INDEX)>=len(test_images):
    INDEX=""

INDEX = int(INDEX)
predicted_value=class_names[np.argmax(prediction[INDEX])] 
actual_value= class_names[test_labels[INDEX][0]]
print(f"Real Value: {actual_value} - Predicted Value: {predicted_value}") 
plt.figure()
plt.imshow(test_images[INDEX])

