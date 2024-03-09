import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def crop_and_merge(image_path, top_crop=100, bottom_crop=100):
    # Load the image
    image = Image.open(image_path)
    image_np = np.array(image)

    # Get the image dimensions
    height, width = image_np.shape[:2]

    # Crop the lower left side with 100px more at the bottom
    lower_left = image_np[height//2 + bottom_crop:, :width//2, :]

    # Crop the upper right side with 100px less at the top
    upper_right = image_np[:height//2 - top_crop, width//2:, :]

    # Calculate the new height after cropping
    new_height = lower_left.shape[0] + upper_right.shape[0]

    # Create an empty canvas with the same width and the new height
    merged_image = np.zeros((new_height, width//2, 3), dtype=np.uint8)

    # Place the cropped regions on the canvas
    merged_image[:lower_left.shape[0], :, :] = lower_left
    merged_image[lower_left.shape[0]:, :, :] = upper_right

    # Convert the result back to RGB
    if image_np.shape[2] == 4:  # Check if the image is RGBA
        merged_image_rgb = cv2.cvtColor(merged_image, cv2.COLOR_BGRA2RGB)
    else:
        merged_image_rgb = cv2.cvtColor(merged_image, cv2.COLOR_BGR2RGB)

    return merged_image_rgb

def count_leaves(cropped_and_merged_image, area_threshold=1000):
    # Convert the cropped and merged image from RGBA to BGR (OpenCV format)
    image_bgr = cv2.cvtColor(cropped_and_merged_image, cv2.COLOR_RGB2BGR)

    # Convert the image to HSV and threshold to get green colors
    lower_green = np.array([30, 30, 30])
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

# Crop and merge the image with adjusted cropping
cropped_and_merged_image = crop_and_merge(image_path, top_crop=-100, bottom_crop=100)

# Count the leaves
num_leaves = count_leaves(cropped_and_merged_image)
print("Number of leaves detected:", num_leaves)
