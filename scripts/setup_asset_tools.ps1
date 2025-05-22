# Installation script for asset optimization tools
# This script installs Python packages needed for asset optimization

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found in PATH. Please install Python 3.8 or newer." -ForegroundColor Red
    exit 1
}

# Create requirements file for asset optimization tools
$requirementsContent = @"
# Image processing
Pillow>=9.0.0  # Python Imaging Library fork
python-resize-image>=1.1.20  # Easy resizing
webp>=0.1.0  # WebP conversion
tinify>=1.5.2  # TinyPNG/TinyJPG API client for compression

# Audio processing
pydub>=0.25.1  # Audio processing

# Video processing
moviepy>=1.0.3  # Video processing

# General utilities
tqdm>=4.64.0  # Progress bars
"@

$requirementsPath = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\scripts\requirements-assets.txt"
$requirementsContent | Out-File -FilePath $requirementsPath -Encoding utf8
Write-Host "Created requirements file at: $requirementsPath" -ForegroundColor Green

# Install the required packages
Write-Host "Installing required Python packages for asset optimization..."
python -m pip install --upgrade pip
python -m pip install -r $requirementsPath

Write-Host "`nPackage installation complete!" -ForegroundColor Cyan

# Create a more complete asset optimizer script
$optimizerPath = "C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\scripts\optimize.py"
$optimizerContent = @"
#!/usr/bin/env python3
"""
TEC Asset Optimizer Script

This script optimizes assets for different deployment targets:
- WordPress
- HuggingFace
- Web general use

Usage:
    python optimize.py --source [source_dir] --target [wordpress|huggingface|web]
"""
import os
import sys
import argparse
import shutil
from pathlib import Path
from tqdm import tqdm

try:
    from PIL import Image
    from resizeimage import resizeimage
except ImportError:
    print("Error: Required packages not installed. Run 'pip install -r requirements-assets.txt'")
    sys.exit(1)

# Constants
MAX_WP_FEATURED_SIZE = (1200, 630)
MAX_WP_THUMBNAIL_SIZE = (150, 150)
MAX_WP_CONTENT_WIDTH = 800
MAX_HF_DIMENSION = 1200
QUALITY = {
    'wordpress': 85,
    'huggingface': 75,
    'web': 85
}

def optimize_image(image_path, target_type, output_dir=None):
    """
    Optimize an image for the specified target platform
    """
    try:
        img = Image.open(image_path)
        img_format = img.format
        
        # Determine output path
        if output_dir:
            output_filename = os.path.basename(image_path)
            output_path = os.path.join(output_dir, output_filename)
            
            # Change extension for WebP if target is HuggingFace
            if target_type == 'huggingface':
                output_path = os.path.splitext(output_path)[0] + '.webp'
        else:
            output_path = image_path  # Overwrite original if no output dir
            
        # Make target directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
        # Process based on target
        if target_type == 'wordpress':
            # Default to content size
            max_width = MAX_WP_CONTENT_WIDTH
            if 'featured' in output_dir:
                img = resizeimage.resize_cover(img, MAX_WP_FEATURED_SIZE)
            elif 'thumbnail' in output_dir:
                img = resizeimage.resize_cover(img, MAX_WP_THUMBNAIL_SIZE)
            else:  # content
                # Resize only if larger than max width
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.LANCZOS)
                    
            # Save with appropriate quality
            img.save(output_path, quality=QUALITY[target_type], optimize=True)
            
        elif target_type == 'huggingface':
            # Resize if larger than max dimension
            if img.width > MAX_HF_DIMENSION or img.height > MAX_HF_DIMENSION:
                if img.width > img.height:
                    ratio = MAX_HF_DIMENSION / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((MAX_HF_DIMENSION, new_height), Image.LANCZOS)
                else:
                    ratio = MAX_HF_DIMENSION / img.height
                    new_width = int(img.width * ratio)
                    img = img.resize((new_width, MAX_HF_DIMENSION), Image.LANCZOS)
            
            # Convert to WebP for better compression
            img.save(output_path, 'WEBP', quality=QUALITY[target_type], method=6)
            
        elif target_type == 'web':
            # General web optimization
            # Resize if larger than 1600px on any dimension
            if img.width > 1600 or img.height > 1600:
                if img.width > img.height:
                    ratio = 1600 / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((1600, new_height), Image.LANCZOS)
                else:
                    ratio = 1600 / img.height
                    new_width = int(img.width * ratio)
                    img = img.resize((new_width, 1600), Image.LANCZOS)
            
            # Determine best format based on content
            if img_format == 'PNG' and has_transparency(img):
                # Keep PNG for transparency
                img.save(output_path, 'PNG', optimize=True)
            else:
                # Use JPEG for photos and other graphics
                output_path = os.path.splitext(output_path)[0] + '.jpg'
                img = img.convert('RGB')
                img.save(output_path, 'JPEG', quality=QUALITY[target_type], optimize=True)
                
        return output_path
            
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def has_transparency(img):
    """Check if image has transparency"""
    if img.info.get('transparency', None) is not None:
        return True
    if img.mode == 'RGBA':
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True
    return False

def process_directory(source_dir, target_type, output_base):
    """Process all images in a directory recursively"""
    source_path = Path(source_dir)
    
    # Determine which output subdirectory to use based on target
    if target_type == 'wordpress':
        output_dirs = {
            'featured': os.path.join(output_base, 'wordpress', 'featured'),
            'thumbnails': os.path.join(output_base, 'wordpress', 'thumbnails'),
            'content': os.path.join(output_base, 'wordpress', 'content')
        }
    elif target_type == 'huggingface':
        output_dirs = {
            'ui': os.path.join(output_base, 'huggingface', 'ui'),
            'images': os.path.join(output_base, 'huggingface', 'images'),
            'icons': os.path.join(output_base, 'huggingface', 'icons')
        }
    elif target_type == 'web':
        output_dirs = {
            'images': os.path.join(output_base, 'web', 'images'),
            'default': os.path.join(output_base, 'web', 'images')
        }
        
    # Create output directories if they don't exist
    for dir_path in output_dirs.values():
        os.makedirs(dir_path, exist_ok=True)
    
    # Find all image files
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
        image_files.extend(list(source_path.glob(f"**/{ext}")))
    
    print(f"Found {len(image_files)} images to process")
    
    # Process each file
    results = {'success': 0, 'error': 0}
    for img_path in tqdm(image_files, desc=f"Optimizing for {target_type}"):
        rel_path = img_path.relative_to(source_path)
        
        # Determine destination directory based on file path or name
        if target_type == 'wordpress':
            if 'featured' in str(rel_path).lower():
                output_dir = output_dirs['featured']
            elif 'thumbnail' in str(rel_path).lower():
                output_dir = output_dirs['thumbnails']
            else:
                output_dir = output_dirs['content']
                
        elif target_type == 'huggingface':
            if 'ui' in str(rel_path).lower() or 'interface' in str(rel_path).lower():
                output_dir = output_dirs['ui']
            elif 'icon' in str(rel_path).lower():
                output_dir = output_dirs['icons']
            else:
                output_dir = output_dirs['images']
                
        else:  # web
            output_dir = output_dirs.get('images', output_dirs['default'])
        
        # Process the image
        result = optimize_image(str(img_path), target_type, output_dir)
        if result:
            results['success'] += 1
        else:
            results['error'] += 1
            
    return results

def main():
    parser = argparse.ArgumentParser(description='Optimize TEC assets for different platforms')
    parser.add_argument('--source', type=str, required=True, help='Source directory containing assets')
    parser.add_argument('--target', type=str, required=True, choices=['wordpress', 'huggingface', 'web'], 
                      help='Target platform for optimization')
    args = parser.parse_args()
    
    # Validate source directory
    if not os.path.isdir(args.source):
        print(f"Error: Source directory not found: {args.source}")
        return 1
        
    # Determine output directory (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.dirname(script_dir)
    output_base = os.path.join(assets_dir, 'optimized')
    
    print(f"Optimizing assets from {args.source} for {args.target}...")
    
    results = process_directory(args.source, args.target, output_base)
    
    print("\nOptimization summary:")
    print(f"- Successfully processed: {results['success']} images")
    print(f"- Errors: {results['error']} images")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
"@

$optimizerContent | Out-File -FilePath $optimizerPath -Encoding utf8
Write-Host "Created enhanced optimizer script at: $optimizerPath" -ForegroundColor Green

Write-Host "`nSetup complete!" -ForegroundColor Cyan
Write-Host "Run the asset optimization with:" -ForegroundColor Yellow
Write-Host "python $optimizerPath --source C:\Users\Ghedd\TEC_CODE\astradigital-engine\assets\source\images --target wordpress" -ForegroundColor Yellow
