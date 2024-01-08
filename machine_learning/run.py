from load import model
from preprocess import preprocess_image
import numpy as np

image_paths = ['path/to/your/new/image.jpg']
for image_path in image_paths:
    preprocessed_image = preprocess_image(image_path)

    predictions = model.predict(preprocessed_image)
    class_labels = ['healthy', 'diseased', 'pest-infested']
    predicted_class = class_labels[np.argmax(predictions)]
    confidence = predictions[0][np.argmax(predictions)]

    print(f"The plant on {image_path} is {predicted_class} with confidence {confidence:.2f}")
