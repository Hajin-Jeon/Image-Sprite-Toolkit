import json
import argparse
from PIL import Image
import os
from rectpack import newPacker, PackingMode, PackingBin

def setup_argparse():
    parser = argparse.ArgumentParser(description="Merge individual images into a sprite sheet.")
    parser.add_argument("-j", "--json", required=True, help="Path to the JSON file defining the images.")
    parser.add_argument("-i", "--images_folder", required=True, help="Path to the folder containing the images.")
    parser.add_argument("-o", "--output", required=True, help="Output path for the resulting sprite sheet.")
    parser.add_argument("--mode", default="manual", choices=['manual', 'automatic'], help="(optional) Mode of image placement: manual or automatic.")
    parser.add_argument("-mw", "--max_width", type=int, default=0, help="(optional) Maximum width of the bin for packing images. Only needs for automatic mode. (Default: 2 * maximum width among the images)")
    return parser.parse_args()

def load_images(images_folder):
    images = []
    for img_filename in os.listdir(images_folder):
        if img_filename.endswith('.png'):
            img_path = os.path.join(images_folder, img_filename)
            img = Image.open(img_path)
            width, height = img.size
            name = os.path.splitext(img_filename)[0]
            images.append((img, name, width, height))
    return images

def manual_position(images, json_data):
    positions = []
    total_width = 0
    total_height = 0
    for item in json_data:
        rect = item['Rectangle']
        x, y, width, height = int(rect['x']), int(rect['y']), int(rect['width']), int(rect['height'])
        total_width = max(total_width, x + width)
        total_height = max(total_height, y + height)
        positions.append((item['name'], x, y, width, height))
    return positions, total_width, total_height

def automatic_position(images, max_width):
    if max_width == 0:
        max_width = max(img.size[0] for img, _, _, _ in images) * 2
    packer = newPacker(mode=PackingMode.Offline, bin_algo=PackingBin.Global, rotation=False)
    for img, name, width, height in images:
        packer.add_rect(width, height, rid=name)
    total_height = sum(img.size[1] for img, _, _, _ in images)
    packer.add_bin(max_width, total_height)
    packer.pack()

    positions = []
    total_width = 0
    total_height = 0
    for rect in packer.rect_list():
        b, x, y, w, h, n = rect

        positions.append((n, x, y, w, h))
        total_width = max(total_width, x + w)
        total_height = max(total_height, y + h)

    for rect in packer.rect_list():
        b, x, y, w, h, n = rect
        print(f"Rect ID: {n}, X: {x}, Y: {y}, Width: {w}, Height: {h}")

    print(len(packer.rect_list()))
    return positions, total_width, total_height

def create_sprite_sheet(images, positions, width, height, output_path):
    image_dict = {name: img for img, name, _, _ in images}

    sprite_sheet = Image.new("RGBA", (width, height))
    for n, x, y, w, h in positions:
        if n in image_dict:
            img = image_dict[n]
            sprite_sheet.paste(img, (x, y))
        else:
            print(f"Warning: Image for '{name}' not found.")
    sprite_sheet.save(output_path)
    print(f"Sprite sheet saved to {output_path}")

def save_positions(positions, output_json):
    data = [{'name': name, 'Rectangle': {'x': x, 'y': y, 'width': w, 'height': h}} for (name, x, y, w, h) in positions]
    with open(output_json, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    args = setup_argparse()
    images = load_images(args.images_folder)
    if args.mode == 'manual':
        with open(args.json, 'r') as f:
            json_data = json.load(f)
        positions, width, height = manual_position(images, json_data)
    elif args.mode == 'automatic':
        positions, width, height = automatic_position(images, args.max_width)
        save_positions(positions, args.json)
    
    create_sprite_sheet(images, positions, width, height, args.output)

if __name__ == "__main__":
    main()