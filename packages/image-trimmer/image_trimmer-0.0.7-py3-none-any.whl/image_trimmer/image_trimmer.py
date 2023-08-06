import os
import argparse
import yaml
from PIL import Image
import pytesseract
import datetime
import re


def crop_image(image_path, crop_template):
    # Open the image file
    image = Image.open(image_path)

    # Crop the image
    cropped_image = image.crop(
        (
            crop_template["x"],
            crop_template["y"],
            crop_template["x"] + crop_template["width"],
            crop_template["y"] + crop_template["height"],
        )
    )

    # Extract text from the cropped image using OCR
    text = pytesseract.image_to_string(cropped_image, lang="tha")
    text = text.split("\n")
    text = text[0]
    text = text.replace(" ", "")
    return cropped_image, text


def crop_images(input_folder, output_folder, template_name):
    name_list = []
    # Define the crop templates
    templates = {
        "scb": {"x": 40, "y": 166, "width": 580, "height": 70},
        "kbank": {"x": 0, "y": 135, "width": 745, "height": 75},
    }

    # Check if the template exists
    if template_name not in templates:
        print(f"Error: template '{template_name}' not found, only supports: scb, kbank")
        return

    # Make the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all files in the input folder
    files = os.listdir(input_folder)

    # Check if any files are images
    image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    image_files = [
        f for f in files if os.path.splitext(f)[1].lower() in image_extensions
    ]

    if not image_files:
        print(f"Warning: no image files found in {input_folder}.")
        return

    # Get the current timestamp
    current_time = datetime.datetime.now()

    # Format the timestamp to yyyy-mm-dd_hh-mm-ss format
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

    # Loop over all image files in the input folder
    for filename in image_files:
        # Open the image file and crop it
        image_path = os.path.join(input_folder, filename)
        cropped_image, text = crop_image(image_path, templates[template_name])

        # Save the cropped image to the output folder
        output_path = os.path.join(
            output_folder, f"""{template_name}_{formatted_time}_{filename}"""
        )
        cropped_image.save(output_path)

        # Save the extracted text to a text file
        text = re.sub("[^A-Za-zก-๙เแไใ]+", "", text)
        name_list.append(text)

    text_path = os.path.join(
        output_folder, f"""{template_name}_{formatted_time}_name_list.txt"""
    )
    with open(text_path, "w", encoding="utf-8") as f:
        f.write("\n".join(name_list))


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Crop images.")
    parser.add_argument(
        "--input_folder", "-i", help="Input folder containing images to crop."
    )
    parser.add_argument(
        "--output_folder", "-o", help="Output folder to save cropped images."
    )
    parser.add_argument(
        "--template", "-t", required=True, help="Name of the crop template to use."
    )
    args = parser.parse_args()

    # Crop the images
    crop_images(args.input_folder, args.output_folder, args.template)


if __name__ == "__main__":
    main()
