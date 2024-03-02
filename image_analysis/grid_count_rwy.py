import os
import cv2
import numpy as np
from PIL import Image
import csv

# Define HSV ranges for white, yellow, and red
hsv_ranges = {
    'white': ((220, 220, 220), (255, 255, 255)),
    'yellow': ((255, 160, 0), (255, 255, 100)),
    'red': ((255, 0, 0), (255, 75, 30)),
}

area_threshold = float(input(f"Enter color area threshold: "))

def crop_image(image, crop_width):
    height, width = image.shape[:2]
    cropped_image = image[:, :width - crop_width, :]
    return cropped_image

def apply_morphological_operations(mask, kernel_size=(7, 7), iterations=2):
    kernel = np.ones(kernel_size, np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel, iterations=iterations)
    return opening

def find_and_draw_contours(image, mask, color, area_threshold, title):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > area_threshold]

    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, filtered_contours, -1, color, 2)

    image_with_contours_rgb = cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB)

    total_pixel_count = sum(cv2.contourArea(cnt) for cnt in filtered_contours)

    return image_with_contours_rgb, filtered_contours, total_pixel_count

def count_objects(image_path):
    image = Image.open(image_path)
    image_np = np.array(image)

    cropped_image = crop_image(image_np, crop_width=100)
    image_bgr = cv2.cvtColor(cropped_image, cv2.COLOR_RGBA2BGR)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    images_with_contours = []
    filtered_contours = []
    total_pixel_counts = []

    for color, (lower, upper) in hsv_ranges.items():
        mask = cv2.inRange(image_hsv, np.array(lower), np.array(upper))
        opening_mask = apply_morphological_operations(mask)

        image_with_contours, contours, total_pixel_count = find_and_draw_contours(image_bgr, opening_mask, get_color_code(color), area_threshold, color)

        images_with_contours.append(image_with_contours)
        filtered_contours.append(contours)
        total_pixel_counts.append(total_pixel_count)

    # Return the number of objects for each color
    num_objects = [len(contours) for contours in filtered_contours]
    return num_objects, total_pixel_counts

def get_color_code(color):
    if color == 'white':
        return (255, 255, 255)
    elif color == 'yellow':
        return (255, 255, 0)
    elif color == 'red':
        return (255, 0, 0)

def process_images_in_directory_and_save_csv(directory_path, output_csv_path):
    num_objects_data = {color: [] for color in hsv_ranges.keys()}
    total_pixel_counts_data = {color: [] for color in hsv_ranges.keys()}

    for filename in os.listdir(directory_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(directory_path, filename)
            num_objects, total_pixel_counts = count_objects(image_path)

            for color, count, total_pixel_count in zip(hsv_ranges.keys(), num_objects, total_pixel_counts):
                num_objects_data[color].append(count)
                total_pixel_counts_data[color].append(total_pixel_count)

    # Save results to CSV
    with open(output_csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header
        header = ['Image Index'] + [f'{color.capitalize()} Num Objects' for color in hsv_ranges.keys()] + [f'{color.capitalize()} Total Pixel Count' for color in hsv_ranges.keys()]
        csv_writer.writerow(header)

        # Write data
        num_images = max(len(num_objects_data[color]) for color in hsv_ranges.keys())
        for i in range(num_images):
            row = [i] + [num_objects_data[color][i] if i < len(num_objects_data[color]) else 0 for color in hsv_ranges.keys()] + [total_pixel_counts_data[color][i] if i < len(total_pixel_counts_data[color]) else 0 for color in hsv_ranges.keys()]
            csv_writer.writerow(row)

# Specify the path to the directory containing images
directory_path = "assets"
output_csv_path = "output_results.csv"

# Process images in the directory and save results to CSV
process_images_in_directory_and_save_csv(directory_path, output_csv_path)
