#!/usr/bin/env python3
"""Resize avatar image for Hedra"""
from PIL import Image
import os

# Open the original image
img_path = "emotion-concept-portrait-angry-cute-asian-woman-standing-posing-with-crossed-arms-looking-camera-with-grey-clothes-white-background.jpg"
img = Image.open(img_path)

print(f"Original size: {img.size}")

# Resize to a reasonable size for avatar (keeping aspect ratio)
# Try 512x768 (portrait orientation)
max_width = 512
max_height = 768

# Calculate new size maintaining aspect ratio
aspect_ratio = img.width / img.height
if aspect_ratio > (max_width / max_height):
    # Width is the limiting factor
    new_width = max_width
    new_height = int(max_width / aspect_ratio)
else:
    # Height is the limiting factor
    new_height = max_height
    new_width = int(max_height * aspect_ratio)

# Resize using high-quality resampling
resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Save the resized image
output_path = "avatar_resized.jpg"
resized.save(output_path, "JPEG", quality=95, optimize=True)

print(f"Resized to: {resized.size}")
print(f"Saved to: {output_path}")
print(f"File size: {os.path.getsize(output_path) / 1024:.2f} KB")
