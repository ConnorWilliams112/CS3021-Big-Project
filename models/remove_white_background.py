#!/usr/bin/env python3
"""
Script to remove white background from duck PNG images and replace with transparency.
This processes all PNG files in the Images directory.
"""

import os
from PIL import Image

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "Images")

def remove_white_background(image_path):
    """
    Remove white background from image and replace with transparency.
    
    Args:
        image_path: Path to the image file
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get image data
        data = img.getdata()
        
        # Process each pixel
        new_data = []
        for item in data:
            # If pixel is white (or very close to white), make it transparent
            # White is (255, 255, 255)
            # Allow some tolerance for anti-aliasing
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                # Replace white with transparent
                new_data.append((255, 255, 255, 0))
            else:
                # Keep other pixels as-is
                new_data.append(item)
        
        # Update image with new data
        img.putdata(new_data)
        
        # Save the image back
        img.save(image_path, "PNG")
        print(f"✓ Processed: {os.path.basename(image_path)}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {image_path}: {e}")
        return False

def main():
    """Process all PNG files in the Images directory."""
    print(f"Looking for PNG files in: {IMAGES_DIR}")
    
    if not os.path.exists(IMAGES_DIR):
        print(f"Error: Images directory not found at {IMAGES_DIR}")
        return
    
    # Get all PNG files in the Images directory
    png_files = [f for f in os.listdir(IMAGES_DIR) if f.endswith('.png')]
    
    if not png_files:
        print("No PNG files found in Images directory")
        return
    
    print(f"Found {len(png_files)} PNG files to process:\n")
    
    # Process each PNG file
    success_count = 0
    for png_file in png_files:
        image_path = os.path.join(IMAGES_DIR, png_file)
        if remove_white_background(image_path):
            success_count += 1
    
    print(f"\n✓ Successfully processed {success_count}/{len(png_files)} images")

if __name__ == "__main__":
    main()
