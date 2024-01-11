import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def crop_image(image, crop_width):
    height, width = image.shape[:2]
    cropped_image = image[:, :width - crop_width, :]
    return cropped_image

def adjust_brightness(image, factor=1.3):
    # Convert the image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Multiply the value channel by the brightness factor
    hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * factor, 0, 255).astype(np.uint8)
    
    # Convert the image back to BGR
    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    
    return adjusted_image

def count_leaves(image_path):
    # Load the image
    image = Image.open(image_path)
    image_np = np.array(image)

    # Crop the image by 100 pixels on the right side
    cropped_image = crop_image(image_np, crop_width=100)

    # Adjust the brightness of the cropped image
    brighter_image = adjust_brightness(cropped_image, factor=1.2)

    # Convert the brighter image from RGBA to BGR (OpenCV format)
    image_bgr = cv2.cvtColor(brighter_image, cv2.COLOR_RGBA2BGR)

    # Convert the image to HSV and threshold to get green colors
    lower_green = np.array([20, 20, 20])
    upper_green = np.array([90, 255, 255])
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image_hsv, lower_green, upper_green)

    # Apply morphological operations
    kernel = np.ones((7, 7), np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    area_threshold = float(input("Enter green area threshold: "))
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > area_threshold]

    # Draw contours on the original image
    image_with_contours = image_bgr.copy()
    cv2.drawContours(image_with_contours, filtered_contours, -1, (0, 255, 0), 2)

    # Convert the result back to RGB
    image_with_contours_rgb = cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB)

    # Calculate total pixel count inside selected areas
    total_pixel_count = sum(cv2.contourArea(cnt) for cnt in filtered_contours)
    print("Total pixel count inside selected areas:", total_pixel_count)

    # Display the result
    plt.imshow(image_with_contours_rgb)
    plt.title('Contours After Filtering')
    plt.axis('off')
    plt.show()

    # Return the number of leaves
    return len(filtered_contours)

# Specify the path to your image
image_path = "test.png"

# Count the leaves
num_leaves = count_leaves(image_path)
print("Number of leaves detected:", num_leaves)
