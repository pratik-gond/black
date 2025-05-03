# Black Image Detector

A Python tool that detects if an image is predominantly of a single color by analyzing pixel values and comparing them to the average color of the image.

## Features

- Detects if an image is predominantly of a single color
- Works with both color (RGB/RGBA) and grayscale images
- Uses average color as reference instead of a single pixel
- Configurable threshold for color similarity
- Performance timing for execution analysis
- Detailed debug output for analysis

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy
- Pillow (PIL)

## Installation

1. Clone the repository
2. Install the required packages:
```bash
pip install opencv-python numpy pillow
```

## Usage

Run the script:
```bash
python black_image_detector.py
```

The program provides an interactive menu with the following options:
1. Check if an image is of a single color
2. Exit

### How it Works

The detector uses the following process:
1. Calculates the average color of the entire image
2. Compares each pixel to the average color
3. Counts how many pixels are within the threshold (default: 20) of the average color
4. If more than 50% of pixels are within threshold, the image is considered single-colored

### Output

The program provides detailed output including:
- Whether the image is single-colored
- The average color value (RGB)
- Processing time in seconds
- Debug information about the image processing

### Threshold Value

The default threshold value is set to 20, which means:
- For RGB images: Each color channel (R,G,B) can differ by up to 20 from the average
- For grayscale images: The pixel value can differ by up to 20 from the average

You can modify the threshold value in the code to be more or less strict in color matching.

## Example Output

```
[DEBUG] Processing image: example.jpg
[DEBUG] Using threshold value: 20
[DEBUG] Image shape: (800, 600, 3)
[DEBUG] Average color (RGB): (45, 45, 45)
[DEBUG] Pixels within threshold: 450000/480000 (93.75%)
[DEBUG] Is single color: True
[DEBUG] Final color value (RGB): (45, 45, 45)
[DEBUG] Execution time: 0.234 seconds

Result: The image is of a single color!
Color (RGB): (45, 45, 45)
Processing time: 0.234 seconds
```

## Performance

The script includes timing functionality to measure:
- Total execution time
- Processing time for each operation
- Time taken for different image sizes and types

This helps in analyzing the performance and optimizing the detection process.

## License

This project is open source and available under the MIT License. 