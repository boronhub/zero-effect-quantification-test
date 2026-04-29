#!/usr/bin/env python3
"""
Script to resolve image paths for Filler entries and copy them to the Filler folder.
Searches all three experiment folders for the image names and copies matches.
"""

import csv
import shutil
import os
from pathlib import Path
from collections import defaultdict

def main():
    # Paths
    csv_path = Path("stimulus_table_all_exps_zh.csv")
    filler_dir = Path("Filler")
    experiment_dirs = {
        'ESQ': Path("Experiment 1 ESQ - pictures"),
        'DIST': Path("Experiment 2 DIST - pictures"),
        'UB': Path("Experiment 3 UB - pictures"),
    }
    
    # Create Filler directory if it doesn't exist
    filler_dir.mkdir(exist_ok=True)
    print(f"Filler directory: {filler_dir.absolute()}")
    
    # Read CSV and extract Filler images
    filler_images = set()
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Experiment', '').strip() == 'Filler':
                image = row.get('Image', '').strip()
                if image:
                    # Handle missing .svg extension (some entries don't have it)
                    if not image.endswith('.svg'):
                        image += '.svg'
                    filler_images.add(image)
    
    print(f"\nTotal unique images in Filler entries: {len(filler_images)}")
    print("\nFiller images to find:")
    for img in sorted(filler_images):
        print(f"  - {img}")
    
    # Build a map of all available images across all experiment folders
    image_locations = defaultdict(list)
    for exp_name, exp_dir in experiment_dirs.items():
        if exp_dir.exists():
            for svg_file in exp_dir.glob("*.svg"):
                image_locations[svg_file.name].append((exp_name, svg_file))
    
    # Copy each Filler image to the Filler directory
    copied = 0
    not_found = []
    
    for image_name in sorted(filler_images):
        if image_name in image_locations:
            exp_name, source_path = image_locations[image_name][0]  # Use first match
            dest_path = filler_dir / image_name
            
            # Copy the file
            shutil.copy2(source_path, dest_path)
            print(f"✓ Copied: {image_name} (from {exp_name} folder)")
            copied += 1
        else:
            not_found.append(image_name)
            print(f"✗ NOT FOUND: {image_name}")
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Copied: {copied} images")
    print(f"  Not found: {len(not_found)} images")
    
    if not_found:
        print(f"\nMissing images:")
        for img in not_found:
            print(f"  - {img}")
    
    print(f"\nImages now in Filler directory: {len(list(filler_dir.glob('*.svg')))}")

if __name__ == '__main__':
    main()
