#!/usr/bin/env python3
"""
Docker Asset Optimizer Script

This script optimizes assets for Docker container deployment by:
1. Reducing image sizes to minimize container footprint
2. Converting images to WebP format for optimal size/quality
3. Preserving appropriate file formats for configuration files

Usage:
    python docker.py --asset [path/to/asset] --type [image|config|static] --output [output_path]
"""

import os
import sys
import argparse
import shutil
from pathlib import Path

try:
    from PIL import Image
    has_pil = True
except ImportError:
    has_pil = False
    print("PIL not available. Images will be copied without optimization.")

def optimize_image(input_path, output_path):
    """Optimize an image for Docker deployment"""
    try:
        if has_pil:
            img = Image.open(input_path)
            
            # Determine output format based on input
            input_format = Path(input_path).suffix.lower()
            
            # Use WebP for most images except SVG
            if input_format not in ['.svg']:
                output_path_webp = os.path.splitext(output_path)[0] + ".webp"
                
                # Reduce size to max 800px width
                width, height = img.size
                if width > 800:
                    ratio = 800.0 / width
                    height = int(height * ratio)
                    width = 800
                    img = img.resize((width, height), Image.LANCZOS)
                
                # Save as WebP with good compression
                img.save(output_path_webp, "WEBP", quality=75)
                return output_path_webp
            else:
                # SVG files should just be copied
                shutil.copy(input_path, output_path)
                return output_path
        else:
            # No PIL available, just copy
            shutil.copy(input_path, output_path)
            return output_path
    except Exception as e:
        print(f"Error optimizing image: {e}")
        shutil.copy(input_path, output_path)
        return output_path

def optimize_static_file(input_path, output_path):
    """Process static files (HTML, CSS, JS)"""
    # For static files, we could implement minification here
    # For now, just copy the file
    shutil.copy(input_path, output_path)
    return output_path

def optimize_config_file(input_path, output_path):
    """Process configuration files"""
    # Config files are just copied as-is
    # We don't want to modify their format
    shutil.copy(input_path, output_path)
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Optimize assets for Docker deployment')
    parser.add_argument('--asset', type=str, required=True, help='Path to source asset')
    parser.add_argument('--type', type=str, required=True, 
                      choices=['image', 'static', 'config'], 
                      help='Type of Docker asset')
    parser.add_argument('--output', type=str, help='Output file path')
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.asset):
        print(f"Error: Asset file not found: {args.asset}")
        return 1
    
    # Make sure output directory exists
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
    else:
        # Create default output path if not specified
        input_path = Path(args.asset)
        output_dir = input_path.parent
        output_path = output_dir / f"{input_path.stem}-docker{input_path.suffix}"
        args.output = str(output_path)
    
    # Process based on type
    if args.type == 'image':
        final_path = optimize_image(args.asset, args.output)
        print(f"Optimized image saved to: {final_path}")
    elif args.type == 'static':
        final_path = optimize_static_file(args.asset, args.output)
        print(f"Processed static file: {final_path}")
    else:  # config
        final_path = optimize_config_file(args.asset, args.output)
        print(f"Processed config file: {final_path}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
