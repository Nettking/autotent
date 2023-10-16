import cv2
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))  # Adjust to the model's input size
    image = image / 255.0  # Normalize pixel values to [0, 1]
    return np.expand_dims(image, axis=0)  # Add batch dimension
