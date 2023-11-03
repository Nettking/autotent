import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def detect_disease(image_path):
    # Load the image
    image = Image.open(image_path)
    image_np = np.array(image)

    # Convert the image from RGBA to BGR (OpenCV format)
    image_rgb = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # Define BGR color range for brown
    lower_brown = np.array([127, 140, 191])  # BGR values
    upper_brown = np.array([143, 180, 255])

    # Threshold the image to get only brown colors
    mask = cv2.inRange(image_bgr, lower_brown, upper_brown)

    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    area_threshold = 50  # You might need to adjust this value
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > area_threshold]

    # Draw contours on the original image
    image_with_contours = image_bgr.copy()
    cv2.drawContours(image_with_contours, filtered_contours, -1, (0, 255, 0), 2)

    # Convert the result back to RGB for displaying
    image_with_contours_rgb = cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB)

    # Display the result
    plt.imshow(image_with_contours_rgb)
    plt.title('Brown Areas Detected')
    plt.axis('off')
    plt.show()

    # Return the number of brown areas detected
    return len(filtered_contours)

# Specify the path to your image
image_path = "test.png"

# Detect disease (brown areas)
num_brown_areas = detect_disease(image_path)
print("Number of brown areas detected:", num_brown_areas)
