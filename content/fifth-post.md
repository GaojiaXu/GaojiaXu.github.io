title: Blog on Homework 5
date: 11/12/2021
author: Gaojia Xu

In this homework, we suppose to train a deep learning model to classify beetles, cockroaches and dragonflies using these [images](https://www.dropbox.com/s/fn73sj2e6c9rhf6/insects.zip?dl=0) and *explain* how the neural network classified the images using [SHapley Additive exPlanations](https://github.com/slundberg/shap).


Blog outline:

* [4.1 Load Data](#section1)
* [4.2 Model training](#section2)
* [4.3 Model Evaluation and Prediction](#section3)



<a name="section1"></a>
##4.1 Load Data

We first read in train set and test set, for simplicity, code below can read images in subdirectories and consider them as category outcome, we also specify batch_size to be 32 which means each batch contains 32 images.


```python

train_ds = image_dataset_from_directory(
    directory='insects/train/',
    labels='inferred', #contain subdirectories, as category outcome
    label_mode='categorical',
    batch_size=32, #each batch contains 32 images
    image_size=(256, 256))
test_ds = image_dataset_from_directory(
    directory='insects/test/',
    labels='inferred',
    label_mode='categorical', 
    batch_size=32,
    image_size=(256, 256))
```

We can see images shown from the train set as well using code below.

```python
plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
    for i in range(9):
        ax = plt.subplot(3, 3, i + 1)
        plt.imshow(images[i].numpy().astype("uint8")) 
```

To produce more training data based on limited size we have, we can make some changes to original dataset named data_augmentation, including such as horizontal flip mode, rotation and zoom, this helps reduce overfitting as well.

```python
img_height = 256
img_width = 256

data_augmentation = keras.Sequential(
  [layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
  ]
)
```

<a name="section2"></a>
##4.2 Model training

1. For input shape of the rescaling: 

- Input_shape is the height, width of the image and RGB 3 channels of the color.

After the first layer, we don't need to specify the size of the input anymore.



2. For convolution parameter:

Different filter will produce different output of an image, such as the darkness of the image, countour of the image and so on, we can comprehend each filter make emphasis on specific characteristic of the image.

- Filter means the total dimensionality of the output space (i.e. the number of filters in the convolution).

- Kernel size means the height and width of the 2D convolution window(which is moving). Can be a single integer to specify the same value for all spatial dimensions, we can specify as 3*3 window by specifying 3.

- Stride is the step of the window is default 1.

- Padding = "same" means we padding with zeros evenly to the left/right or up/down of the input in order to make image length/width divisible by step length of the convolution window. 

- We choose relu activation function for easier training and better performance.

3. MaxPooling can be seen as the resizing of the image, while reduce dimention, it still keeps major important features. Default is 2x2 pooling window.

4. Dropout randomly drops out (by setting the activation to zero) a number of output units from the layer during the training process to avoid overfitting, we can set it to 0.2.

5. Flatten is used after convolution, to make inputs from more than 2 dimensional matrix to 2 dimension.

6. Dense specifies units = dimensionality of the output space.


```python
num_classes =3

model = Sequential([
  data_augmentation,
  layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.2),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

```

Since we have 3 categories(more than 2), we can use specify CategoricalCrossentropy as loss function, label represented by float numbers.

```python
model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
              

```

Then we train our model, we specify epochs to be 20 because passing the whole training data only one time is not enough, we have to update weights several times, since each batch has 32 images, we have 32 batches since whole train set has 1019 files (1019/32=31.8).

```python
epochs=25
history = model.fit(
  train_ds,
  validation_data=test_ds,
  epochs=epochs
)
```

<a name="section3"></a>
##4.3 Model Evaluation and Prediction


```python
fig, axes = plt.subplots(1,2,figsize=(12, 4))
for ax, measure in zip(axes, ['loss', 'accuracy']):
    ax.plot(history.history[measure], label=measure)
    ax.plot(history.history['val_' + measure], label='val_' + measure)
    ax.legend()
pass

```

The loss is decreasing and accuracy is increasing as epoch increases. The loss and accuracy of test set is orange line, slightly worse than the blue line but there is no huge discrepancy.

We can test one image from the dragonfly category, the prediction score of 3 classes can be obtained by using below code.

```python
image_size = (256,256)

img = keras.preprocessing.image.load_img("Insects/test/dragonflies/5402448.jpg", 
                                         target_size=image_size)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create batch axis

predictions = model.predict(img_array)

```

From below code, we will see the output pixels of the images about the 3 classes. Red pixels increase the model output to be one class while blue pixels decrease the output.


```python
X_train = np.concatenate([x for x, y in train_ds], axis=0)
y_train = np.concatenate([y for x, y in train_ds], axis=0)
X_test = np.concatenate([x for x, y in test_ds], axis=0)
y_test = np.concatenate([y for x, y in test_ds], axis=0)

import shap
explainer = shap.GradientExplainer(model, X_train)
sv = explainer.shap_values(X_test[175:180]);
shap.image_plot([sv[i] for i in range(len(sv))], X_test[175:180])

```

Take the fourth image as an example, we have already checked from the prediction that this is a dragonfly, and from a direct look it is a dragonfly as well. Based on the plots in the fourth line, we see the third one has most redness compared to others, where there are activations indicating how the CNN distinguishes between these outcomes.



