#!/usr/bin/env python3
"""
WordPress Asset Preparation Script

This script prepares assets for a WordPress post by:
1. Optimizing source images for WordPress
2. Generating featured image, thumbnails, and content images
3. Preparing a package ready for WordPress upload

Usage:
    python prepare_wp_assets.py --post "Post Title" --source [source_dir]
"""

import os
import sys
import argparse
import logging
import shutil
import json
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TEC.AssetPrep")

# Constants
ASSETS_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
OPTIMIZED_DIR = os.path.join(ASSETS_ROOT, "optimized", "wordpress")
DEPLOYMENT_DIR = os.path.join(ASSETS_ROOT, "deployment", "wordpress")

def slugify(text):
    """Convert text to slug format"""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def optimize_for_wordpress(source_dir, post_slug):
    """Optimize images in source directory for WordPress"""
    # Create post-specific subdirectories
    timestamp = datetime.now().strftime("%Y%m%d")
    post_dir = f"{timestamp}-{post_slug}"
    
    featured_dir = os.path.join(OPTIMIZED_DIR, "featured", post_dir)
    thumbnail_dir = os.path.join(OPTIMIZED_DIR, "thumbnails", post_dir)
    content_dir = os.path.join(OPTIMIZED_DIR, "content", post_dir)
    
    os.makedirs(featured_dir, exist_ok=True)
    os.makedirs(thumbnail_dir, exist_ok=True)
    os.makedirs(content_dir, exist_ok=True)
    
    # Find source images
    source_path = Path(source_dir)
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
        image_files.extend(list(source_path.glob(f"**/{ext}")))
    
    if not image_files:
        logger.warning(f"No images found in {source_dir}")
        return None
        
    logger.info(f"Found {len(image_files)} images to process")
    
    # Process each image using the optimize script
    results = {
        'featured': [],
        'thumbnails': [],
        'content': []
    }
    
    # Path to optimizer script
    optimizer_script = os.path.join(ASSETS_ROOT, "scripts", "wordpress.py")
    
    # First image becomes featured image by default
    first_img = image_files[0]
    featured_output = os.path.join(featured_dir, f"{post_slug}-featured{first_img.suffix}")
    
    # Run optimizer in separate process
    import subprocess
    logger.info(f"Creating featured image from {first_img}")
    
    try:
        subprocess.run([
            sys.executable, optimizer_script,
            "--image", str(first_img),
            "--type", "featured",
            "--output", featured_output
        ], check=True)
        results['featured'].append(featured_output)
    except subprocess.CalledProcessError:
        logger.error(f"Failed to create featured image from {first_img}")
        # Fallback: copy the original
        shutil.copy(str(first_img), featured_output)
        results['featured'].append(featured_output)
    
    # Create thumbnail for first image
    thumbnail_output = os.path.join(thumbnail_dir, f"{post_slug}-thumb{first_img.suffix}")
    logger.info(f"Creating thumbnail from {first_img}")
    
    try:
        subprocess.run([
            sys.executable, optimizer_script,
            "--image", str(first_img),
            "--type", "thumbnail",
            "--output", thumbnail_output
        ], check=True)
        results['thumbnails'].append(thumbnail_output)
    except subprocess.CalledProcessError:
        logger.error(f"Failed to create thumbnail from {first_img}")
    
    # Process all images as content images
    for i, img_path in enumerate(image_files):
        img_name = f"{post_slug}-{i+1}{img_path.suffix}"
        content_output = os.path.join(content_dir, img_name)
        
        logger.info(f"Creating content image from {img_path}")
        try:
            subprocess.run([
                sys.executable, optimizer_script,
                "--image", str(img_path),
                "--type", "content",
                "--output", content_output
            ], check=True)
            results['content'].append(content_output)
        except subprocess.CalledProcessError:
            logger.error(f"Failed to create content image from {img_path}")
            # Fallback: copy the original
            shutil.copy(str(img_path), content_output)
            results['content'].append(content_output)
    
    return results

def prepare_deployment_package(results, post_title, post_slug):
    """Prepare a deployment package with all optimized assets"""
    timestamp = datetime.now().strftime("%Y%m%d")
    deploy_dir = os.path.join(DEPLOYMENT_DIR, f"{timestamp}-{post_slug}")
    os.makedirs(deploy_dir, exist_ok=True)
    
    # Copy all optimized assets to deployment directory
    all_files = []
    for category, file_list in results.items():
        category_dir = os.path.join(deploy_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        for file_path in file_list:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(category_dir, filename)
            shutil.copy(file_path, dest_path)
            all_files.append({
                'category': category,
                'filename': filename,
                'path': dest_path
            })
    
    # Create metadata file
    metadata = {
        'post_title': post_title,
        'post_slug': post_slug,
        'created': datetime.now().isoformat(),
        'files': all_files,
        'stats': {
            'featured': len(results['featured']),
            'thumbnails': len(results['thumbnails']),
            'content': len(results['content']),
            'total': len(all_files)
        }
    }
    
    metadata_path = os.path.join(deploy_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Create HTML snippet for easy copy-paste into WordPress
    html_content = []
    html_content.append(f"<!-- TEC Asset Package: {post_title} -->")
    html_content.append("<div class='tec-image-gallery'>")
    
    for file_info in [f for f in all_files if f['category'] == 'content']:
        filename = file_info['filename']
        rel_path = os.path.join('wp-content', 'uploads', timestamp, filename)
        html_content.append(f"  <img src='{rel_path}' alt='{filename}' class='tec-content-image' />")
    
    html_content.append("</div>")
    
    html_path = os.path.join(deploy_dir, 'wordpress-snippet.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_content))
    
    return deploy_dir

def main():
    parser = argparse.ArgumentParser(description='Prepare assets for WordPress post')
    parser.add_argument('--post', type=str, required=True, help='Post title')
    parser.add_argument('--source', type=str, required=True, help='Source directory containing assets')
    args = parser.parse_args()
    
    # Validate source directory
    if not os.path.isdir(args.source):
        logger.error(f"Source directory not found: {args.source}")
        return 1
    
    # Create slug from post title
    post_slug = slugify(args.post)
    
    logger.info(f"Preparing assets for post: {args.post}")
    logger.info(f"Post slug: {post_slug}")
    
    # Check if WordPress.py exists
    wp_script = os.path.join(ASSETS_ROOT, "scripts", "wordpress.py")
    if not os.path.exists(wp_script):
        # Create minimal version for this script to work
        os.makedirs(os.path.dirname(wp_script), exist_ok=True)
        with open(wp_script, 'w') as f:
            f.write('''
#!/usr/bin/env python3
"""
WordPress Asset Optimizer Script
"""
import os
import sys
import argparse
from pathlib import Path
import shutil

def main():
    parser = argparse.ArgumentParser(description='Optimize images for WordPress')
    parser.add_argument('--image', type=str, required=True, help='Path to source image')
    parser.add_argument('--type', type=str, required=True, 
                      choices=['featured', 'thumbnail', 'content'], 
                      help='Type of WordPress image to create')
    parser.add_argument('--output', type=str, help='Output file path')
    args = parser.parse_args()
    
    # Make the output directory if it doesn't exist
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        # For now, just copy the file (no optimization without PIL)
        shutil.copy(args.image, args.output)
    else:
        # Create output path from input path
        input_path = Path(args.image)
        output_dir = input_path.parent
        output_path = output_dir / f"{input_path.stem}-{args.type}{input_path.suffix}"
        shutil.copy(args.image, output_path)
        
    return 0

if __name__ == '__main__':
    sys.exit(main())
''')
        logger.info(f"Created basic wordpress.py script at {wp_script}")

    # Optimize source images
    results = optimize_for_wordpress(args.source, post_slug)
    if not results:
        logger.error("Failed to optimize images for WordPress")
        return 1
    
    # Create deployment package
    deploy_path = prepare_deployment_package(results, args.post, post_slug)
    
    logger.info(f"WordPress asset package created: {deploy_path}")
    logger.info(f"- Featured images: {len(results['featured'])}")
    logger.info(f"- Thumbnails: {len(results['thumbnails'])}")
    logger.info(f"- Content images: {len(results['content'])}")
    logger.info(f"HTML snippet available at: {os.path.join(deploy_path, 'wordpress-snippet.html')}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
