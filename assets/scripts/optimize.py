#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEC Asset Optimization Script
=============================

A multi-purpose tool for optimizing assets (images, audio, etc.) for different platforms:
- WordPress (featured images, thumbnails, content images)
- HuggingFace (web-optimized assets)
- Docker (deployment-ready assets)

Author: TEC Development Team
"""

import os
import sys
import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

try:
    from PIL import Image
    import webp
    from tqdm import tqdm
except ImportError:
    print("Required packages are missing. Please install with:")
    print("pip install Pillow webp tqdm")
    sys.exit(1)

# Configuration
IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
CONFIG = {
    "wordpress": {
        "featured": {
            "max_width": 1200,
            "max_height": 630,
            "quality": 85
        },
        "thumbnail": {
            "max_width": 150,
            "max_height": 150,
            "quality": 80
        },
        "content": {
            "max_width": 800,
            "max_height": None,  # Preserve aspect ratio
            "quality": 85
        }
    },
    "huggingface": {
        "ui": {
            "max_width": 800,
            "max_height": None,  # Preserve aspect ratio
            "quality": 85,
            "format": "webp"
        },
        "images": {
            "max_width": 1200,
            "max_height": None,  # Preserve aspect ratio
            "quality": 75,
            "format": "webp"
        },
        "icons": {
            "max_width": 256,
            "max_height": 256,
            "quality": 85,
            "format": "webp"
        }
    },
    "web": {
        "general": {
            "max_width": 1600,
            "max_height": None,  # Preserve aspect ratio
            "quality": 80,
            "format": "webp"
        },
        "thumbnails": {
            "max_width": 400, 
            "max_height": None,
            "quality": 80,
            "format": "webp"
        }
    },
    "docker": {
        "general": {
            "max_width": 800,
            "max_height": None,
            "quality": 75,
            "format": "webp"
        }
    }
}

def setup_argparse():
    """Set up command line arguments."""
    parser = argparse.ArgumentParser(
        description="TEC Asset Optimization Tool - Optimize assets for different platforms",
        epilog="Example: python optimize.py --source assets/source/images --platform wordpress"
    )
    
    parser.add_argument(
        "--source", 
        required=True,
        help="Source directory containing assets to optimize"
    )
    
    parser.add_argument(
        "--output",
        help="Output directory for optimized assets (default: assets/optimized/[platform])"
    )
    
    parser.add_argument(
        "--platform",
        choices=["wordpress", "huggingface", "web", "docker", "all"],
        default="all",
        help="Target platform for optimization"
    )
    
    parser.add_argument(
        "--type",
        choices=["images", "audio", "video", "all"],
        default="images",
        help="Type of assets to optimize"
    )
    
    parser.add_argument(
        "--quality",
        type=int,
        choices=range(1, 101),
        default=None,
        help="Override quality setting (1-100)"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively process all files in subdirectories"
    )
    
    return parser.parse_args()

def get_output_dir(base_dir, platform, asset_type):
    """Get the appropriate output directory based on platform and asset type."""
    if platform == "wordpress":
        if asset_type == "featured":
            return os.path.join(base_dir, "wordpress", "featured")
        elif asset_type == "thumbnail":
            return os.path.join(base_dir, "wordpress", "thumbnails")
        else:
            return os.path.join(base_dir, "wordpress", "content")
    elif platform == "huggingface":
        if asset_type == "ui":
            return os.path.join(base_dir, "huggingface", "ui")
        elif asset_type == "icons":
            return os.path.join(base_dir, "huggingface", "icons")
        else:
            return os.path.join(base_dir, "huggingface", "images")
    elif platform == "web":
        if asset_type == "thumbnails":
            return os.path.join(base_dir, "web", "thumbnails")
        else:
            return os.path.join(base_dir, "web", "images")
    elif platform == "docker":
        return os.path.join(base_dir, "docker", "images")
    
    # Default fallback
    return os.path.join(base_dir, platform, asset_type)

def optimize_image(source_path, output_path, config, quality_override=None):
    """Optimize an image according to the configuration."""
    try:
        img = Image.open(source_path)
        
        # Get dimensions from config
        max_width = config.get("max_width")
        max_height = config.get("max_height")
        quality = quality_override if quality_override is not None else config.get("quality", 85)
        output_format = config.get("format", "jpeg").upper()
        
        # Resize if needed
        width, height = img.size
        if max_width and width > max_width:
            if max_height:
                # Both dimensions constrained
                new_width = max_width
                new_height = max_height
                img = img.resize((new_width, new_height), Image.LANCZOS)
            else:
                # Only width is constrained, maintain aspect ratio
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.LANCZOS)
        elif max_height and height > max_height:
            # Only height is constrained, maintain aspect ratio
            ratio = max_height / height
            new_width = int(width * ratio)
            img = img.resize((new_width, max_height), Image.LANCZOS)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert and save optimized image
        if output_format == "WEBP":
            if img.mode in ("RGBA", "LA"):
                # Preserve transparency
                img.save(output_path, "WEBP", quality=quality, lossless=False, method=5)
            else:
                # Convert to RGB for WebP
                img = img.convert("RGB")
                img.save(output_path, "WEBP", quality=quality, lossless=False, method=5)
        else:
            # For other formats like JPEG, PNG
            if output_format == "JPEG" and img.mode in ("RGBA", "LA"):
                # JPEG doesn't support transparency, convert to RGB
                img = img.convert("RGB")
            
            img.save(output_path, output_format, quality=quality, optimize=True)
            
        return True
    except Exception as e:
        print(f"Error optimizing {source_path}: {str(e)}")
        return False

def get_output_filename(source_filename, platform, asset_type):
    """Generate an appropriate output filename based on platform and asset type."""
    name, ext = os.path.splitext(source_filename)
    
    # Check if we need to change the extension
    if platform in CONFIG and asset_type in CONFIG[platform]:
        output_format = CONFIG[platform][asset_type].get("format")
        if output_format:
            ext = f".{output_format.lower()}"
    
    return f"{name}{ext}"

def find_assets(source_dir, asset_type="images", recursive=False):
    """Find assets of the specified type in the source directory."""
    assets = []
    
    if asset_type == "images":
        extensions = IMAGE_FORMATS
    elif asset_type == "audio":
        extensions = [".mp3", ".wav", ".ogg", ".flac"]
    elif asset_type == "video":
        extensions = [".mp4", ".webm", ".ogv"]
    else:
        extensions = []
    
    # Get all files with specified extensions
    source_path = Path(source_dir)
    
    if recursive:
        for ext in extensions:
            assets.extend(list(source_path.glob(f"**/*{ext}")))
    else:
        for ext in extensions:
            assets.extend(list(source_path.glob(f"*{ext}")))
    
    return assets

def optimize_for_platform(source_dir, output_base, platform, asset_type="images", 
                         quality_override=None, verbose=False, dry_run=False, recursive=False):
    """Optimize assets for a specific platform."""
    stats = {
        "platform": platform,
        "asset_type": asset_type,
        "total": 0,
        "optimized": 0,
        "skipped": 0,
        "errors": 0
    }
    
    # Find assets
    assets = find_assets(source_dir, asset_type, recursive)
    stats["total"] = len(assets)
    
    if stats["total"] == 0:
        print(f"No {asset_type} found in {source_dir}")
        return stats
    
    if verbose:
        print(f"Found {stats['total']} {asset_type} in {source_dir}")
    
    # Process assets based on platform
    if platform == "wordpress":
        for asset in tqdm(assets, desc="Optimizing for WordPress"):
            # Process for each WordPress asset type
            for wp_type in ["featured", "thumbnail", "content"]:
                output_dir = get_output_dir(output_base, platform, wp_type)
                output_filename = get_output_filename(asset.name, platform, wp_type)
                output_path = os.path.join(output_dir, output_filename)
                
                if os.path.exists(output_path) and not dry_run:
                    stats["skipped"] += 1
                    if verbose:
                        print(f"Skipping {output_path} (already exists)")
                    continue
                
                if dry_run:
                    print(f"Would optimize: {asset} -> {output_path}")
                    continue
                
                config = CONFIG["wordpress"][wp_type]
                success = optimize_image(str(asset), output_path, config, quality_override)
                
                if success:
                    stats["optimized"] += 1
                    if verbose:
                        print(f"Optimized: {asset} -> {output_path}")
                else:
                    stats["errors"] += 1
    
    elif platform == "huggingface":
        for asset in tqdm(assets, desc="Optimizing for HuggingFace"):
            # Try to determine asset type based on path or name
            path_str = str(asset).lower()
            
            if 'ui' in path_str or 'interface' in path_str or 'button' in path_str:
                hf_type = 'ui'
            elif 'icon' in path_str or asset.suffix == '.svg':
                hf_type = 'icons'
            else:
                hf_type = 'images'
            
            output_dir = get_output_dir(output_base, platform, hf_type)
            output_filename = get_output_filename(asset.name, platform, hf_type)
            output_path = os.path.join(output_dir, output_filename)
            
            if os.path.exists(output_path) and not dry_run:
                stats["skipped"] += 1
                if verbose:
                    print(f"Skipping {output_path} (already exists)")
                continue
            
            if dry_run:
                print(f"Would optimize: {asset} -> {output_path}")
                continue
            
            config = CONFIG["huggingface"][hf_type]
            success = optimize_image(str(asset), output_path, config, quality_override)
            
            if success:
                stats["optimized"] += 1
                if verbose:
                    print(f"Optimized: {asset} -> {output_path}")
            else:
                stats["errors"] += 1
    
    elif platform == "web":
        for asset in tqdm(assets, desc="Optimizing for Web"):
            # Check if it's a thumbnail
            path_str = str(asset).lower()
            web_type = "thumbnails" if "thumbnail" in path_str else "general"
            
            output_dir = get_output_dir(output_base, platform, web_type)
            output_filename = get_output_filename(asset.name, platform, web_type)
            output_path = os.path.join(output_dir, output_filename)
            
            if os.path.exists(output_path) and not dry_run:
                stats["skipped"] += 1
                if verbose:
                    print(f"Skipping {output_path} (already exists)")
                continue
            
            if dry_run:
                print(f"Would optimize: {asset} -> {output_path}")
                continue
            
            config = CONFIG["web"][web_type]
            success = optimize_image(str(asset), output_path, config, quality_override)
            
            if success:
                stats["optimized"] += 1
                if verbose:
                    print(f"Optimized: {asset} -> {output_path}")
            else:
                stats["errors"] += 1
    
    elif platform == "docker":
        for asset in tqdm(assets, desc="Optimizing for Docker"):
            output_dir = get_output_dir(output_base, platform, "general")
            output_filename = get_output_filename(asset.name, platform, "general")
            output_path = os.path.join(output_dir, output_filename)
            
            if os.path.exists(output_path) and not dry_run:
                stats["skipped"] += 1
                if verbose:
                    print(f"Skipping {output_path} (already exists)")
                continue
            
            if dry_run:
                print(f"Would optimize: {asset} -> {output_path}")
                continue
            
            config = CONFIG["docker"]["general"]
            success = optimize_image(str(asset), output_path, config, quality_override)
            
            if success:
                stats["optimized"] += 1
                if verbose:
                    print(f"Optimized: {asset} -> {output_path}")
            else:
                stats["errors"] += 1
    
    return stats

def save_stats(stats, output_base):
    """Save optimization statistics to a log file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(output_base, f"optimization_log_{timestamp}.json")
    
    stats["timestamp"] = datetime.now().isoformat()
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    return log_path

def main():
    """Main function."""
    args = setup_argparse()
    
    # Set up directories
    source_dir = os.path.abspath(args.source)
    
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory {source_dir} does not exist.")
        sys.exit(1)
    
    # Default output directory is assets/optimized/[platform]
    if args.output:
        output_base = os.path.abspath(args.output)
    else:
        # Determine the root assets directory (assuming we're in scripts or assets/scripts)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.basename(script_dir) == "scripts":
            if os.path.basename(os.path.dirname(script_dir)) == "assets":
                # We're in assets/scripts
                assets_dir = os.path.dirname(script_dir)
            else:
                # We're in scripts directory, assume parent is the root
                assets_dir = os.path.dirname(script_dir)
        else:
            # We're somewhere else, just use the current directory
            assets_dir = os.path.dirname(script_dir)
        
        output_base = os.path.join(assets_dir, "optimized")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_base, exist_ok=True)
    
    # Process assets
    all_stats = []
    platforms = CONFIG.keys() if args.platform == "all" else [args.platform]
    
    for platform in platforms:
        print(f"Processing assets for {platform}...")
        stats = optimize_for_platform(
            source_dir, 
            output_base, 
            platform, 
            args.type,
            args.quality, 
            args.verbose, 
            args.dry_run,
            args.recursive
        )
        all_stats.append(stats)
        
        print(f"- Total: {stats['total']}")
        print(f"- Optimized: {stats['optimized']}")
        print(f"- Skipped: {stats['skipped']}")
        print(f"- Errors: {stats['errors']}\n")
    
    # Save logs if not a dry run
    if not args.dry_run and all_stats:
        log_path = save_stats(all_stats, output_base)
        print(f"Optimization log saved to: {log_path}")
    
    print("Optimization complete!")

if __name__ == "__main__":
    main()
