from PIL import Image

def split_and_save_images(input_image, output_image_prefix):
    # Open the image
    original_image = Image.open(input_image)

    # Get the width and height
    width, height = original_image.size

    # Split the image into 4 equal parts
    top_right = original_image.crop((width // 2 + width // 5, 0, width, height // 2 - height // 10))
    bottom_left = original_image.crop((width // 3, height // 4, width, height))


    # Create empty images with the same dimensions
    new_image_1 = Image.new('RGB', (width // 2, height // 2))
    new_image_2 = Image.new('RGB', (width // 2, height // 2))

    # Paste the top-right and bottom-left parts into the new images
    new_image_1.paste(top_right, (0, 0))
    new_image_2.paste(bottom_left, (0, 0))

    # Save the resulting images with suffixes 1 and 2
    output_image_1 = output_image_prefix + "_1.jpg"
    output_image_2 = output_image_prefix + "_2.jpg"
    new_image_1.save(output_image_1)
    new_image_2.save(output_image_2)

    print("Images split and saved to", output_image_1, "and", output_image_2)

if __name__ == "__main__":
    input_image = "input.png"  # Replace with the path to your image
    output_image_prefix = "output"  # Replace with the desired prefix for the new images

    split_and_save_images(input_image, output_image_prefix)
