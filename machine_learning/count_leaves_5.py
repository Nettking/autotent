import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

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
    print(f"Total pixel count inside selected areas for {title}: {total_pixel_count}")

    return image_with_contours_rgb, filtered_contours

def count_leaves(image_path):
    image = Image.open(image_path)
    image_np = np.array(image)

    cropped_image = crop_image(image_np, crop_width=100)
    image_bgr = cv2.cvtColor(cropped_image, cv2.COLOR_RGBA2BGR)
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # Define HSV ranges for light green, medium green, and dark green
    hsv_ranges = {
        'light_green': ((30, 85, 30), (90, 255, 255)),
        'medium_green': ((40, 30, 30), (70, 85, 255)),
        'dark_green': ((30, 30, 30), (90, 85, 255)),
    }

    images_with_contours = []
    filtered_contours = []
    area_threshold = float(input(f"Enter color area threshold: "))
    for color, (lower, upper) in hsv_ranges.items():
        mask = cv2.inRange(image_hsv, np.array(lower), np.array(upper))
        opening_mask = apply_morphological_operations(mask)
        image_with_contours, contours = find_and_draw_contours(image_bgr, opening_mask, get_color_code(color), area_threshold, color)

        images_with_contours.append(image_with_contours)
        filtered_contours.append(contours)

    # Display the results
    plt.figure(figsize=(12, 4))

    for i, (title, image) in enumerate(zip(hsv_ranges.keys(), images_with_contours), 1):
        plt.subplot(1, 3, i)
        plt.imshow(image)
        plt.title(f'Contours After Filtering ({title.capitalize()})')
        plt.axis('off')

    plt.show()

    # Return the number of leaves for each color
    num_leaves = [len(contours) for contours in filtered_contours]
    return num_leaves

def get_color_code(color):
    if color == 'light_green':
        return (0, 255, 0)
    elif color == 'medium_green':
        return (0, 255, 255)
    elif color == 'dark_green':
        return (0, 0, 255)

# Specify the path to your image
image_path = "test.png"

# Count the leaves for light green, medium green, and dark green separately
num_leaves = count_leaves(image_path)

for color, count in zip(['Light Green', 'Medium Green', 'Dark Green'], num_leaves):
    print(f"Number of leaves detected ({color}): {count}")
