import tensorflow as tf
import os
import datetime
import time
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np

# Define the downsample and upsample functions
def downsample(filters, size, apply_batchnorm=True):
    initializer = tf.random_normal_initializer(0., 0.02)

    result = tf.keras.Sequential()
    result.add(
        tf.keras.layers.Conv2D(filters, size, strides=2, padding='same',
                                kernel_initializer=initializer, use_bias=False))

    if apply_batchnorm:
        result.add(tf.keras.layers.BatchNormalization())

    result.add(tf.keras.layers.LeakyReLU())

    return result

def upsample(filters, size, apply_dropout=False):
    initializer = tf.random_normal_initializer(0., 0.02)

    result = tf.keras.Sequential()
    result.add(
        tf.keras.layers.Conv2DTranspose(filters, size, strides=2,
                                        padding='same',
                                        kernel_initializer=initializer,
                                        use_bias=False))

    result.add(tf.keras.layers.BatchNormalization())

    if apply_dropout:
        result.add(tf.keras.layers.Dropout(0.5))

    result.add(tf.keras.layers.ReLU())

    return result

# The checkpoint directory
checkpoint_dir = '/checkpointDir'

# Set up the Generator
OUTPUT_CHANNELS = 3

def Generator():
    inputs = tf.keras.layers.Input(shape=[256, 256, 3])

    down_stack = [
        downsample(64, 4, apply_batchnorm=False),  # (batch_size, 128, 128, 64)
        downsample(128, 4),  # (batch_size, 64, 64, 128)
        downsample(256, 4),  # (batch_size, 32, 32, 256)
    ]

    up_stack = [
        upsample(256, 4),  # (batch_size, 64, 64, 256)
        upsample(128, 4),  # (batch_size, 128, 128, 128)
        upsample(64, 4),  # (batch_size, 256, 256, 64)
    ]

    initializer = tf.random_normal_initializer(0., 0.02)
    last = tf.keras.layers.Conv2DTranspose(OUTPUT_CHANNELS, 4,
                                           strides=2,
                                           padding='same',
                                           kernel_initializer=initializer,
                                           activation='tanh')  # (batch_size, 256, 256, 3)

    x = inputs

    # Downsampling through the model
    skips = []
    for down in down_stack:
        x = down(x)
        skips.append(x)

    skips = reversed(skips[:-1])

    # Upsampling and establishing the skip connections
    for up, skip in zip(up_stack, skips):
        x = up(x)
        x = tf.keras.layers.Concatenate()([x, skip])

    x = last(x)

    return tf.keras.Model(inputs=inputs, outputs=x)

# Create the generator model
generator = Generator()

# Create a checkpoint object to restore the generator
checkpoint = tf.train.Checkpoint(generator=generator)

# Restore the latest checkpoint
checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))

def load_and_preprocess_image(image_path):
    # Load the image using PIL
    img = Image.open(image_path)

    # Preprocess the image (e.g., resize to 256x256, convert to numpy array, normalize)
    img = img.resize((256, 256))
    img = np.array(img) / 127.5 - 1
    img = tf.expand_dims(img, axis=0)

    return img

def predict(image_path, save_path):
    # Load and preprocess the input image
    input_image = load_and_preprocess_image(image_path)

    # Generate the output image using the generator
    output_image = generator(input_image, training=False)

    # Denormalize the output image to [0, 255] range
    output_image = (output_image[0].numpy() + 1) * 127.5
    output_image = output_image.astype(np.uint8)

    # Save the generated image
    generated_image = Image.fromarray(output_image)
    generated_image.save(save_path)

    print("sucess")
    return True