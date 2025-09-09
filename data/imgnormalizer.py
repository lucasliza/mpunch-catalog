#!/usr/bin/env python3
"""
Script to remove images from data folder that are not referenced in JSON file.
"""

import json
import os
import sys
from pathlib import Path
from typing import Set, List


def load_json_data(json_file_path: str) -> List[dict]:
    """Load and parse JSON data from file."""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        sys.exit(1)


def extract_referenced_images(json_data: List[dict]) -> Set[str]:
    """Extract all image filenames referenced in the JSON data."""
    referenced_images = set()
    
    for item in json_data:
        if 'image_url' in item and item['image_url']:
            # Extract filename from the path (handle both forward and backward slashes)
            image_path = item['image_url']
            filename = os.path.basename(image_path.replace('\\', '/'))
            if filename:  # Only add non-empty filenames
                referenced_images.add(filename)
    
    return referenced_images


def get_images_in_folder(folder_path: str) -> Set[str]:
    """Get all image files in the specified folder."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        sys.exit(1)
    
    # Common image extensions
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
    
    images_in_folder = set()
    folder = Path(folder_path)
    
    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            images_in_folder.add(file_path.name)
    
    return images_in_folder


def remove_unused_images(folder_path: str, referenced_images: Set[str], dry_run: bool = False) -> None:
    """Remove images that are not referenced in the JSON data."""
    images_in_folder = get_images_in_folder(folder_path)
    unused_images = images_in_folder - referenced_images
    
    if not unused_images:
        print("No unused images found. All images are referenced in the JSON data.")
        return
    
    print(f"Found {len(unused_images)} unused image(s):")
    for image in sorted(unused_images):
        print(f"  - {image}")
    
    if dry_run:
        print(f"\nDry run mode: No files were actually deleted.")
        return
    
    # Ask for confirmation
    response = input(f"\nDo you want to delete these {len(unused_images)} unused images? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    # Delete unused images
    deleted_count = 0
    for image in unused_images:
        image_path = Path(folder_path) / image
        try:
            image_path.unlink()
            deleted_count += 1
            print(f"Deleted: {image}")
        except OSError as e:
            print(f"Error deleting {image}: {e}")
    
    print(f"\nSuccessfully deleted {deleted_count} unused images.")


def main():
    """Main function to orchestrate the image cleanup process."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Remove unused images from data folder')
    parser.add_argument('json_file', help='Path to JSON file containing image references')
    parser.add_argument('data_folder', help='Path to folder containing images')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be deleted without actually deleting')
    
    args = parser.parse_args()
    
    print(f"Loading JSON data from: {args.json_file}")
    json_data = load_json_data(args.json_file)
    
    print(f"Extracting referenced images...")
    referenced_images = extract_referenced_images(json_data)
    print(f"Found {len(referenced_images)} referenced images in JSON.")
    
    print(f"Scanning folder: {args.data_folder}")
    images_in_folder = get_images_in_folder(args.data_folder)
    print(f"Found {len(images_in_folder)} images in folder.")
    
    remove_unused_images(args.data_folder, referenced_images, args.dry_run)


if __name__ == "__main__":
    main()