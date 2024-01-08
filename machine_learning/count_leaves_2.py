import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Set the area threshold outside the function
area_threshold = float(input("Enter green area threshold: "))

def count_leaves(image_path):
    # Load the image
    image = Image.open(image_path)
    image_np = np.array(image)

    # Convert the image from RGBA to BGR (OpenCV format)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)

    # Convert the image to HSV and threshold to get only green colors
    lower_green = np.array([30, 40, 40])
    upper_green = np.array([90, 255, 255])
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image_hsv, lower_green, upper_green)

    # Apply morphological operations
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on the area threshold
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > area_threshold]

    # Calculate total pixel count inside selected areas
    total_pixel_count = 0
    for cnt in filtered_contours:
        total_pixel_count += cv2.contourArea(cnt)

    # Return the number of leaves and total pixel count
    return len(filtered_contours), total_pixel_count

def process_images(folder_path):
    # Get a list of all files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Sort the image files from oldest to newest
    image_files.sort()

    # Lists to store data for plotting
    image_names = []
    pixel_counts = []

    # Process each image in the folder
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)

        # Count the leaves for each image
        num_leaves, total_pixel_count = count_leaves(image_path)

        # Store data for plotting
        image_names.append(image_file)
        pixel_counts.append(total_pixel_count)

    # Create a bar graph
    plt.plot(image_names, pixel_counts)
    plt.xlabel('Image Name')
    plt.ylabel('Total Pixel Count')
    plt.title('Total Pixel Count in Selected Areas for Each Image')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Specify the path to your folder containing images
folder_path = "C:\\dev\\autotent\\machine_learning\\assets"

# Process images and create a graph
process_images(folder_path)
