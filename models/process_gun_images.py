#!/usr/bin/env python3
"""
Script to remove white/brown background from gun PNG images and replace with transparency.
Processes 6rds.png through 0rds.png images based on RGB color similarity.
"""

import os
from PIL import Image

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "Images")

def color_distance(c1, c2):
    """Calculate Euclidean distance between two RGB colors."""
    return ((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)**0.5

def remove_background(image_path, tolerance=50):
    """
    Remove white/brown/tan background from image and replace with transparency.
    Analyzes the corner pixels to determine the background color.
    
    Args:
        image_path: Path to the image file
        tolerance: Color distance tolerance for what counts as "background"
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Get a sample of the background color from image corners
        width, height = img.size
        corner_pixels = [
            img.getpixel((0, 0)),
            img.getpixel((width-1, 0)),
            img.getpixel((0, height-1)),
            img.getpixel((width-1, height-1))
        ]
        
        # Use the most common corner color as the background color (first one as baseline)
        bg_color = corner_pixels[0][:3]  # Get RGB only
        
        # Get image data
        data = img.getdata()
        
        # Process each pixel
        new_data = []
        for item in data:
            # Calculate distance from this pixel to the background color
            if len(item) == 4:
                pixel_rgb = item[:3]
            else:
                pixel_rgb = item
            
            distance = color_distance(pixel_rgb, bg_color)
            
            # If pixel is similar to background color, make it transparent
            if distance < tolerance:
                new_data.append((255, 255, 255, 0))  # Transparent
            else:
                new_data.append(item if len(item) == 4 else (*pixel_rgb, 255))
        
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
    """Process all gun images (6rds through 0rds)."""
    print(f"Processing gun images in: {IMAGES_DIR}\n")
    
    if not os.path.exists(IMAGES_DIR):
        print(f"Error: Images directory not found at {IMAGES_DIR}")
        return
    
    # Gun images to process
    gun_images = ['6rds.png', '5rds.png', '4rds.png', '3rds.png', '2rds.png', '1rds.png', '0rds.png']
    
    success_count = 0
    for gun_image in gun_images:
        image_path = os.path.join(IMAGES_DIR, gun_image)
        if os.path.exists(image_path):
            if remove_background(image_path):
                success_count += 1
        else:
            print(f"✗ File not found: {gun_image}")
    
    print(f"\n✓ Successfully processed {success_count}/{len(gun_images)} gun images")

if __name__ == "__main__":
    main()
