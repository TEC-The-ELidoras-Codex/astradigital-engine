#!/usr/bin/env python3
"""
HuggingFace Asset Preparation Script

This script prepares assets for HuggingFace Space deployment by:
1. Optimizing source images for HuggingFace
2. Creating a deployment package with proper structure
3. Generating configuration files for easy import

Usage:
    python prepare_hf_assets.py --name [space_name] --source [source_dir]
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
logger = logging.getLogger("TEC.HFAssetPrep")

# Constants
ASSETS_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
OPTIMIZED_DIR = os.path.join(ASSETS_ROOT, "optimized", "huggingface")
DEPLOYMENT_DIR = os.path.join(ASSETS_ROOT, "deployment", "huggingface")

def optimize_for_huggingface(source_dir, space_name):
    """Optimize images in source directory for HuggingFace"""
    # Create space-specific subdirectories
    timestamp = datetime.now().strftime("%Y%m%d")
    space_dir = f"{timestamp}-{space_name}"
    
    ui_dir = os.path.join(OPTIMIZED_DIR, "ui", space_dir)
    images_dir = os.path.join(OPTIMIZED_DIR, "images", space_dir)
    icons_dir = os.path.join(OPTIMIZED_DIR, "icons", space_dir)
    
    os.makedirs(ui_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(icons_dir, exist_ok=True)
    
    # Find source images
    source_path = Path(source_dir)
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.svg']:
        image_files.extend(list(source_path.glob(f"**/{ext}")))
    
    if not image_files:
        logger.warning(f"No images found in {source_dir}")
        return None
        
    logger.info(f"Found {len(image_files)} images to process")
    
    # Process each image using the optimize script
    results = {
        'ui': [],
        'images': [],
        'icons': []
    }
    
    # Path to optimizer script
    optimizer_script = os.path.join(ASSETS_ROOT, "scripts", "huggingface.py")
    
    # Categorize images based on path or name
    for img_path in image_files:
        img_category = 'images'  # Default category
        img_name = img_path.name.lower()
        
        # Try to determine category from path or filename
        path_str = str(img_path).lower()
        
        if 'ui' in path_str or 'interface' in path_str or 'button' in path_str or 'menu' in path_str:
            img_category = 'ui'
        elif 'icon' in path_str or img_path.suffix == '.svg' or img_name.startswith('icon-'):
            img_category = 'icons'
        
        output_dir = locals().get(f"{img_category}_dir")
        output_file = os.path.join(output_dir, img_path.name)
        
        # Run optimizer in separate process
        logger.info(f"Processing {img_path} as {img_category}")
        
        try:
            import subprocess
            subprocess.run([
                sys.executable, optimizer_script,
                "--asset", str(img_path),
                "--type", img_category,
                "--output", output_file
            ], check=True)
            results[img_category].append(output_file)
        except subprocess.CalledProcessError:
            logger.error(f"Failed to optimize {img_path}")
            # Fallback: copy the original
            shutil.copy(str(img_path), output_file)
            results[img_category].append(output_file)
    
    return results

def prepare_deployment_package(results, space_name):
    """Prepare a deployment package for HuggingFace Space"""
    timestamp = datetime.now().strftime("%Y%m%d")
    deploy_dir = os.path.join(DEPLOYMENT_DIR, f"{timestamp}-{space_name}")
    os.makedirs(deploy_dir, exist_ok=True)
    
    # Create subdirectories for assets
    os.makedirs(os.path.join(deploy_dir, "ui"), exist_ok=True)
    os.makedirs(os.path.join(deploy_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(deploy_dir, "icons"), exist_ok=True)
    
    # Copy all optimized assets to deployment directory
    all_files = []
    total_size = 0
    
    for category, file_list in results.items():
        category_dir = os.path.join(deploy_dir, category)
        
        for file_path in file_list:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(category_dir, filename)
            shutil.copy(file_path, dest_path)
            
            file_size = os.path.getsize(file_path)
            total_size += file_size
            
            all_files.append({
                'category': category,
                'filename': filename,
                'path': dest_path,
                'size': file_size
            })
    
    # Create metadata file
    metadata = {
        'space_name': space_name,
        'created': datetime.now().isoformat(),
        'files': all_files,
        'stats': {
            'ui': len([f for f in all_files if f['category'] == 'ui']),
            'images': len([f for f in all_files if f['category'] == 'images']),
            'icons': len([f for f in all_files if f['category'] == 'icons']),
            'total_files': len(all_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }
    }
    
    metadata_path = os.path.join(deploy_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    # Create Python import script for easy use in HF Space
    import_content = [
        "# Asset imports for HuggingFace Space",
        "# Generated by TEC Asset System",
        "import os",
        "",
        "# Asset paths",
        "ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')",
        "",
        "# UI Assets",
    ]
    
    for f in [f for f in all_files if f['category'] == 'ui']:
        var_name = f['filename'].split('.')[0].upper().replace('-', '_')
        path = os.path.join('ui', f['filename'])
        import_content.append(f"{var_name}_PATH = os.path.join(ASSETS_DIR, '{path}')")
    
    import_content.append("")
    import_content.append("# Image Assets")
    
    for f in [f for f in all_files if f['category'] == 'images']:
        var_name = f['filename'].split('.')[0].upper().replace('-', '_')
        path = os.path.join('images', f['filename'])
        import_content.append(f"{var_name}_PATH = os.path.join(ASSETS_DIR, '{path}')")
    
    import_content.append("")
    import_content.append("# Icon Assets")
    
    for f in [f for f in all_files if f['category'] == 'icons']:
        var_name = f['filename'].split('.')[0].upper().replace('-', '_')
        path = os.path.join('icons', f['filename'])
        import_content.append(f"{var_name}_PATH = os.path.join(ASSETS_DIR, '{path}')")
    
    import_path = os.path.join(deploy_dir, 'asset_paths.py')
    with open(import_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(import_content))
    
    # Create HTML example for use in Gradio
    html_content = [
        "<!-- Example HTML for using assets in Gradio -->",
        "<!-- Include this in your gr.HTML component -->",
        "<div class='tec-assets'>",
    ]
    
    for f in [f for f in all_files if f['category'] == 'ui']:
        html_content.append(f"  <img src='file={{UI_{f['filename'].split('.')[0].upper().replace('-', '_')}_PATH}}' alt='{f['filename']}' class='tec-ui-element' />")
    
    html_content.append("</div>")
    
    html_path = os.path.join(deploy_dir, 'gradio-example.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_content))
    
    # Create deployment guide
    guide_content = f"""# HuggingFace Space Assets - {space_name}

## Overview

This package contains optimized assets for the "{space_name}" HuggingFace Space.

- **Total files**: {metadata['stats']['total_files']}
- **Total size**: {metadata['stats']['total_size_mb']} MB
- **UI elements**: {metadata['stats']['ui']}
- **Images**: {metadata['stats']['images']}
- **Icons**: {metadata['stats']['icons']}

## Usage Instructions

1. Copy the entire `assets` directory to your HuggingFace Space repository
2. Copy `asset_paths.py` to your repository root
3. Import asset paths in your app:

```python
from asset_paths import *

# Use in Gradio components
with gr.Blocks() as demo:
    with gr.Row():
        gr.Image(UI_LOGO_PATH, show_label=False)
```

4. Or use the HTML example in `gradio-example.html` with string formatting

## Size Optimization

If your Space is approaching size limits:

1. Remove unused assets
2. Further compress images (try WebP format)
3. Use external CDN for larger assets

## Generated on {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}
"""
    
    guide_path = os.path.join(deploy_dir, 'README.md')
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    return deploy_dir

def main():
    parser = argparse.ArgumentParser(description='Prepare assets for HuggingFace Space')
    parser.add_argument('--name', type=str, required=True, help='HuggingFace Space name')
    parser.add_argument('--source', type=str, required=True, help='Source directory containing assets')
    args = parser.parse_args()
    
    # Validate source directory
    if not os.path.isdir(args.source):
        logger.error(f"Source directory not found: {args.source}")
        return 1
    
    logger.info(f"Preparing assets for HuggingFace Space: {args.name}")
    
    # Check if huggingface.py exists
    hf_script = os.path.join(ASSETS_ROOT, "scripts", "huggingface.py")
    if not os.path.exists(hf_script):
        # Create minimal version for this script to work
        os.makedirs(os.path.dirname(hf_script), exist_ok=True)
        with open(hf_script, 'w') as f:
            f.write('''
#!/usr/bin/env python3
"""
HuggingFace Asset Optimizer Script
"""
import os
import sys
import argparse
import shutil
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Optimize assets for HuggingFace')
    parser.add_argument('--asset', type=str, required=True, help='Path to source asset')
    parser.add_argument('--type', type=str, required=True, 
                      choices=['ui', 'image', 'icon'], 
                      help='Type of HuggingFace asset')
    parser.add_argument('--output', type=str, help='Output file path')
    args = parser.parse_args()
    
    # For now, just copy the file (no optimization)
    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        shutil.copy(args.asset, args.output)
    else:
        input_path = Path(args.asset)
        output_dir = input_path.parent
        output_path = output_dir / f"{input_path.stem}-hf{input_path.suffix}"
        shutil.copy(args.asset, output_path)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
''')
        logger.info(f"Created basic huggingface.py script at {hf_script}")

    # Optimize source images
    results = optimize_for_huggingface(args.source, args.name)
    if not results:
        logger.error("Failed to optimize assets for HuggingFace")
        return 1
    
    # Create deployment package
    deploy_path = prepare_deployment_package(results, args.name)
    
    logger.info(f"HuggingFace asset package created: {deploy_path}")
    logger.info(f"- UI elements: {len(results['ui'])}")
    logger.info(f"- Images: {len(results['images'])}")
    logger.info(f"- Icons: {len(results['icons'])}")
    logger.info(f"Deployment guide available at: {os.path.join(deploy_path, 'README.md')}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
