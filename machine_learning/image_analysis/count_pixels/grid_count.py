import os
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import csv


# Define HSV ranges for light green, medium green, and dark green
hsv_ranges = {
    'light_green': ((30, 85, 30), (90, 255, 255)),
    'medium_green': ((40, 30, 30), (70, 85, 255)),
    'dark_green': ((30, 30, 30), (90, 85, 255)),
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
    #print(f"Total pixel count inside selected areas for {title}: {total_pixel_count}")

    return image_with_contours_rgb, filtered_contours, total_pixel_count

def count_leaves(image_path):
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

    # Return the number of leaves for each color
    num_leaves = [len(contours) for contours in filtered_contours]
    return num_leaves, total_pixel_counts

def get_color_code(color):
    if color == 'light_green':
        return (144, 255, 144)
    elif color == 'medium_green':
        return (0, 255, 255)
    elif color == 'dark_green':
        return (0, 0, 255)

def process_images_in_directory(directory_path):
    num_leaves_data = {color: [] for color in hsv_ranges.keys()}
    total_pixel_counts_data = {color: [] for color in hsv_ranges.keys()}

    for filename in os.listdir(directory_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(directory_path, filename)
            num_leaves, total_pixel_counts = count_leaves(image_path)

            for color, count, total_pixel_count in zip(hsv_ranges.keys(), num_leaves, total_pixel_counts):
                num_leaves_data[color].append(count)
                total_pixel_counts_data[color].append(total_pixel_count)

    return num_leaves_data, total_pixel_counts_data

def plot_line_graph(data, xlabel, ylabel, title):
    plt.figure(figsize=(10, 6))

    colors = {
                'light_green': (144/255, 255/255, 144/255),  
                'medium_green': (62/255, 155/255, 12/255),  
                'dark_green': (1/255, 100/255, 32/255)       
            }

    for color, values in data.items():
        non_zero_values = [value for value in values if value != 0]
        plt.plot(non_zero_values, label=f'{color.capitalize()}', color=colors[color])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()

def process_images_in_directory_and_save_csv(directory_path, output_csv_path):
    num_leaves_data = {color: [] for color in hsv_ranges.keys()}
    total_pixel_counts_data = {color: [] for color in hsv_ranges.keys()}

    for filename in os.listdir(directory_path):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            image_path = os.path.join(directory_path, filename)
            num_leaves, total_pixel_counts = count_leaves(image_path)

            

            for color, count, total_pixel_count in zip(hsv_ranges.keys(), num_leaves, total_pixel_counts):
                num_leaves_data[color].append(count)
                total_pixel_counts_data[color].append(total_pixel_count)

    # Save results to CSV
    with open(output_csv_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write header
        header = ['Image Index'] + [f'{color.capitalize()} Num Leaves' for color in hsv_ranges.keys()] + [f'{color.capitalize()} Total Pixel Count' for color in hsv_ranges.keys()]
        csv_writer.writerow(header)

        # Write data
        num_images = max(len(num_leaves_data[color]) for color in hsv_ranges.keys())
        for i in range(num_images):
            row = [i] + [num_leaves_data[color][i] if i < len(num_leaves_data[color]) else 0 for color in hsv_ranges.keys()] + [total_pixel_counts_data[color][i] if i < len(total_pixel_counts_data[color]) else 0 for color in hsv_ranges.keys()]
            csv_writer.writerow(row)

# Specify the path to the directory containing images
directory_path = "assets"
output_csv_path = "output_results.csv"

# Process images in the directory and save results to CSV
process_images_in_directory_and_save_csv(directory_path, output_csv_path)


# Specify the path to the directory containing images
directory_path = "assets"

# Process images in the directory
num_leaves_data, total_pixel_counts_data = process_images_in_directory(directory_path)

# Plot line graphs
#plot_line_graph(num_leaves_data, xlabel='Image Index', ylabel='Number of Leaves', title='Number of Leaves in Each Image')
plot_line_graph(total_pixel_counts_data, xlabel='Number of days', ylabel='Total Pixel Count', title='Total Pixel Count in Each Image')
