import cv2
import numpy as np
import os
from PIL import Image
import time

def is_single_color_image(image_path, threshold=20):
    """
    Check if an image is of a single color by comparing pixels to the average color.
    An image is considered single-colored if more than 50% of pixels are within threshold
    of the average color.
    
    Args:
        image_path (str): Path to the image file
        threshold (int): Threshold value for considering pixels as the same color (0-255)
        
    Returns:
        tuple: (bool, tuple, float) - (True if single color, color value in RGB, execution time in seconds)
    """
    start_time = time.time()
    print(f"\n[DEBUG] Processing image: {image_path}")
    print(f"[DEBUG] Using threshold value: {threshold}")
    
    try:
        # Read image using PIL
        print("[DEBUG] Opening image with PIL...")
        img = Image.open(image_path)
        img_array = np.array(img)
        print(f"[DEBUG] Image shape: {img_array.shape}")
        print(f"[DEBUG] Image type: {img_array.dtype}")
        
        # Handle different image formats
        if len(img_array.shape) == 3:  # Color image (RGB/RGBA)
            print("[DEBUG] Processing color image (RGB/RGBA)")
            # Calculate average color
            avg_color = np.mean(img_array[:, :, :3], axis=(0,1)).astype(int)
            print(f"[DEBUG] Average color (RGB): {avg_color}")
            
            # Calculate color difference for each pixel
            print("[DEBUG] Calculating color differences...")
            color_diff = np.abs(img_array[:, :, :3] - avg_color)
            max_diff = np.max(color_diff)
            print(f"[DEBUG] Maximum color difference found: {max_diff}")
            
            # Count pixels within threshold
            pixels_within_threshold = np.sum(np.all(color_diff <= threshold, axis=2))
            total_pixels = img_array.shape[0] * img_array.shape[1]
            percentage_within_threshold = (pixels_within_threshold / total_pixels) * 100
            
            print(f"[DEBUG] Pixels within threshold: {pixels_within_threshold}/{total_pixels} ({percentage_within_threshold:.2f}%)")
            
            # Check if more than 50% of pixels are within threshold
            is_single_color = percentage_within_threshold > 50
            print(f"[DEBUG] Is single color: {is_single_color}")
            
            # Convert average color to RGB tuple
            color_rgb = tuple(avg_color)
            print(f"[DEBUG] Final color value (RGB): {color_rgb}")
            
            execution_time = time.time() - start_time
            print(f"[DEBUG] Execution time: {execution_time:.3f} seconds")
            return is_single_color, color_rgb, execution_time
            
        elif len(img_array.shape) == 2:  # Grayscale image
            print("[DEBUG] Processing grayscale image")
            # Calculate average grayscale value
            avg_value = np.mean(img_array).astype(int)
            print(f"[DEBUG] Average grayscale value: {avg_value}")
            
            # Calculate differences
            differences = np.abs(img_array - avg_value)
            max_diff = np.max(differences)
            print(f"[DEBUG] Maximum difference found: {max_diff}")
            
            # Count pixels within threshold
            pixels_within_threshold = np.sum(differences <= threshold)
            total_pixels = img_array.shape[0] * img_array.shape[1]
            percentage_within_threshold = (pixels_within_threshold / total_pixels) * 100
            
            print(f"[DEBUG] Pixels within threshold: {pixels_within_threshold}/{total_pixels} ({percentage_within_threshold:.2f}%)")
            
            # Check if more than 50% of pixels are within threshold
            is_single_color = percentage_within_threshold > 50
            print(f"[DEBUG] Is single color: {is_single_color}")
            
            # Convert grayscale to RGB tuple
            color_rgb = (avg_value, avg_value, avg_value)
            print(f"[DEBUG] Final color value (RGB): {color_rgb}")
            
            execution_time = time.time() - start_time
            print(f"[DEBUG] Execution time: {execution_time:.3f} seconds")
            return is_single_color, color_rgb, execution_time
            
        else:
            print(f"[DEBUG] Unsupported image format with shape: {img_array.shape}")
            print("Error: Unsupported image format.")
            execution_time = time.time() - start_time
            print(f"[DEBUG] Execution time: {execution_time:.3f} seconds")
            return False, None, execution_time
            
    except FileNotFoundError:
        print(f"[DEBUG] File not found error for: {image_path}")
        print(f"Error: Image file not found at '{image_path}'")
        execution_time = time.time() - start_time
        print(f"[DEBUG] Execution time: {execution_time:.3f} seconds")
        return False, None, execution_time
    except Exception as e:
        print(f"[DEBUG] Unexpected error: {str(e)}")
        print(f"Error processing image: {str(e)}")
        execution_time = time.time() - start_time
        print(f"[DEBUG] Execution time: {execution_time:.3f} seconds")
        return False, None, execution_time

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"[DEBUG] Current directory: {current_dir}")
    
    # Create a directory for test images if it doesn't exist
    test_dir = os.path.join(current_dir, "test_images")
    os.makedirs(test_dir, exist_ok=True)
    print(f"[DEBUG] Test images directory: {test_dir}")
    
    print("\nSingle Color Image Detector")
    print("-------------------------")
    
    while True:
        print("\nOptions:")
        print("1. Check if an image is of a single color")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        print(f"[DEBUG] User choice: {choice}")
        
        if choice == "1":
            image_path = input("Enter the path to the image file: ")
            print(f"[DEBUG] User provided image path: {image_path}")
            
            if not os.path.exists(image_path):
                print("[DEBUG] File does not exist")
                print("Error: File does not exist!")
                continue
            
            is_single_color, color, execution_time = is_single_color_image(image_path)
            
            if is_single_color:
                print(f"Result: The image is of a single color!")
                print(f"Color (RGB): {color}")
            else:
                print("Result: The image contains multiple colors.")
            print(f"Processing time: {execution_time:.3f} seconds")
                
        elif choice == "2":
            print("[DEBUG] User chose to exit")
            print("Goodbye!")
            break
            
        else:
            print(f"[DEBUG] Invalid choice: {choice}")
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()