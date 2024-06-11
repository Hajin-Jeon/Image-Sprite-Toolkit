# Image Sprite Toolkit

This toolkit automates image sprite tasks to facilitate image manipulation and composition. The toolkit consists of two main scripts: `image_parse.py`, and `image_merge.py`.

The toolkit utilizes the [Pillow (PIL)](https://python-pillow.org) for image processing tasks, and [`rectpack`](https://github.com/secnot/rectpack) for optimizing image arrangement in the image merging process.

## Installation

This project requires Python 3.6 or higher. It has been tested specifically on Python 3.7.

Before using the scripts, you must install the necessary Python packages. Use the following command to install the dependencies:

```bash
pip install pillow rectpack
```

## Input JSON Format
The input JSON should follow this structure, which is used by image_parse.py to identify and crop images from a sprite:
```json
[
    {
        "name": "image1",
        "Rectangle": {
            "x": 0,
            "y": 0,
            "width": 100,
            "height": 100
        }
    },
    {
        "name": "image2",
        "Rectangle": {
            "x": 100,
            "y": 100,
            "width": 200,
            "height": 200
        }
    }
]
```
This format ensures that each image segment is correctly identified and processed.

## Usage Instructions

### 1. `image_parse.py`

This script reads image position data from a JSON file to crop the corresponding images from a sprite image and saves them.

**Usage:**

```bash
python image_parse.py -j <json_file> -s <sprite_image> -o <output_folder>
```

- `-j, --json`: JSON file containing the image positions.
- `-s, --sprite`: Source sprite image file.
- `-o, --output`: Folder where cropped images will be saved.

### 2. `image_merge.py`

This script merges individual images into a sprite sheet. It supports two modes: `manual` and `automatic`.

**Usage:**

```bash
python image_merge.py [--mode <mode> -mw <maximum_width>] -i <images_folder> -o <output_sprite> -j <positions_json> 
```

- `--mode`: (Optional) Mode of image merging (`manual` or `automatic`). Default is `manual`.
- `-mw, --max_width`: (Optional) Maximum width of the bin for packing images. Only needs for automatic mode. Default is 2 * maximum width among the images.
- `-i, --images_folder`: Folder containing individual images.
- `-o, --output`: File path for the resulting sprite image.
- `-j, --json`: (In Manual mode) Input JSON file for storing position data. (In Automatic mode) Output JSON file for storing position data.

## Contributor Information

This toolkit was developed by Hajin Jeon. For improvements and bug reports, please submit through the project's GitHub issue tracker.
