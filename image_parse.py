import json
import argparse
from PIL import Image
import os

def setup_argparse():
    parser = argparse.ArgumentParser(description="Extract images from a sprite sheet based on JSON data.")
    parser.add_argument("-j", "--json", required=True, help="Path to the JSON file containing the image definitions.")
    parser.add_argument("-s", "--sprite", required=True, help="Path to the sprite image file.")
    parser.add_argument("-o", "--output", required=True, help="Output directory to save the extracted images.")
    return parser.parse_args()

# validate JSON file
def validate_json(data):
    for item in data:
        if "name" not in item or "Rectangle" not in item or \
           "x" not in item["Rectangle"] or "y" not in item["Rectangle"] or \
           "width" not in item["Rectangle"] or "height" not in item["Rectangle"]:
            raise ValueError("JSON format is incorrect. Expected format example: \n"
                             '{\n'
                             ' "name": "first", \n'
                             ' "Rectangle": {\n'
                             '  "x": 0.0,\n'
                             '  "y": 0.0,\n'
                             '  "width": 384.0,\n'
                             '  "height": 128.0\n'
                             ' }\n'
                             '},\n'
                             '{\n'
                             ' "name": "second", \n'
                             ' "Rectangle": {\n'
                             '  "x": 384.0,\n'
                             '  "y": 0.0,\n'
                             '  "width": 384.0,\n'
                             '  "height": 128.0\n'
                             ' }\n'
                             '}')

# JSON parse
def parse_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

# image extract - save
def extract_and_save_images(data, sprite_image_path, output_folder):
    # create folder if not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created directory {output_folder}")

    sprite_image = Image.open(sprite_image_path)
    for item in data:
        name = item['name']
        rect = item['Rectangle']
        x = int(rect['x'])
        y = int(rect['y'])
        width = int(rect['width'])
        height = int(rect['height'])

        cropped_image = sprite_image.crop((x, y, x + width, y + height))
        
        output_path = f"{output_folder}/{name}.png"
        cropped_image.save(output_path)
        print(f"Image {name} saved to {output_path}")

def main():
    args = setup_argparse()
    
    try:
        with open(args.json, 'r') as file:
            data = json.load(file)
        validate_json(data)
        extract_and_save_images(data, args.sprite, args.output)
    except json.JSONDecodeError as e:
        print(f"An error occurred while parsing the JSON file: {e}")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()