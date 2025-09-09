#!/usr/bin/env python3
"""
Script to normalize image filenames by removing hash codes and updating JSON references.
Removes everything after the last underscore before the file extension.
"""

import json
import os
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


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


def save_json_data(json_file_path: str, data: List[dict], backup: bool = True) -> None:
    """Save JSON data to file with optional backup."""
    if backup:
        backup_path = f"{json_file_path}.backup"
        shutil.copy2(json_file_path, backup_path)
        print(f"Created backup: {backup_path}")
    
    try:
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        sys.exit(1)


def normalize_filename(filename: str) -> str:
    """
    Remove hash code from filename (everything after the last underscore before extension).
    
    Example: 
    '1860-12-26_a-merry-christmas_Desconhecido_6733e6c8a768333c2576e98d.png' 
    becomes '1860-12-26_a-merry-christmas_Desconhecido.png'
    """
    if not filename:
        return filename
    
    # Split filename and extension
    name_part, extension = os.path.splitext(filename)
    
    # Find the last underscore
    last_underscore_idx = name_part.rfind('_')
    
    if last_underscore_idx == -1:
        # No underscore found, return original filename
        return filename
    
    # Remove everything after the last underscore
    normalized_name = name_part[:last_underscore_idx]
    
    return f"{normalized_name}{extension}"


def normalize_image_path(image_path: str) -> str:
    """Normalize the image path by updating the filename part."""
    if not image_path:
        return image_path
    
    # Handle both forward and backward slashes
    path_parts = image_path.replace('\\', '/').split('/')
    filename = path_parts[-1]
    
    # Normalize the filename
    normalized_filename = normalize_filename(filename)
    
    # Reconstruct the path with normalized filename
    path_parts[-1] = normalized_filename
    normalized_path = '/'.join(path_parts)
    
    # Convert back to original slash style (preserve backslashes if they were used)
    if '\\' in image_path:
        normalized_path = normalized_path.replace('/', '\\')
    
    return normalized_path


def get_file_operations(json_data: List[dict], data_folder: str) -> List[Tuple[str, str, int]]:
    """
    Get list of file operations needed (old_path, new_path, json_index).
    Returns list of tuples: (old_file_path, new_file_path, json_record_index)
    """
    operations = []
    data_folder_path = Path(data_folder)
    
    for idx, item in enumerate(json_data):
        if 'image_url' not in item or not item['image_url']:
            continue
        
        # Extract current filename from image_url
        current_path = item['image_url']
        current_filename = os.path.basename(current_path.replace('\\', '/'))
        
        # Generate normalized filename
        normalized_filename = normalize_filename(current_filename)
        
        # Skip if filename doesn't need normalization
        if current_filename == normalized_filename:
            continue
        
        # Build full file paths
        old_file_path = data_folder_path / current_filename
        new_file_path = data_folder_path / normalized_filename
        
        # Check if old file exists
        if not old_file_path.exists():
            print(f"Warning: File not found: {old_file_path}")
            continue
        
        # Check if new filename would conflict with existing file
        if new_file_path.exists() and new_file_path != old_file_path:
            print(f"Warning: Target filename already exists: {new_file_path}")
            continue
        
        operations.append((str(old_file_path), str(new_file_path), idx))
    
    return operations


def preview_operations(operations: List[Tuple[str, str, int]], json_data: List[dict]) -> None:
    """Preview the operations that will be performed."""
    if not operations:
        print("No files need normalization.")
        return
    
    print(f"\nFound {len(operations)} files to normalize:\n")
    
    for old_path, new_path, json_idx in operations:
        old_filename = os.path.basename(old_path)
        new_filename = os.path.basename(new_path)
        
        print(f"File: {old_filename}")
        print(f"  -> {new_filename}")
        print(f"  JSON record #{json_idx + 1}: {json_data[json_idx].get('title', 'N/A')}")
        print()


def perform_normalization(json_file_path: str, data_folder: str, dry_run: bool = False) -> None:
    """Perform the complete normalization process."""
    print(f"Loading JSON data from: {json_file_path}")
    json_data = load_json_data(json_file_path)
    
    print(f"Analyzing files in: {data_folder}")
    operations = get_file_operations(json_data, data_folder)
    
    preview_operations(operations, json_data)
    
    if not operations:
        return
    
    if dry_run:
        print("Dry run mode: No files or JSON would be modified.")
        return
    
    # Ask for confirmation
    response = input(f"Do you want to proceed with normalizing {len(operations)} files? (y/N): ")
    if response.lower() not in ['y', 'yes']:
        print("Operation cancelled.")
        return
    
    # Perform file renaming and JSON updates
    print("\nProcessing files...")
    success_count = 0
    
    for old_path, new_path, json_idx in operations:
        try:
            # Rename the file
            os.rename(old_path, new_path)
            
            # Update JSON data
            old_image_url = json_data[json_idx]['image_url']
            new_image_url = normalize_image_path(old_image_url)
            json_data[json_idx]['image_url'] = new_image_url
            
            print(f"✓ Renamed: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error processing {os.path.basename(old_path)}: {e}")
    
    if success_count > 0:
        print(f"\nSaving updated JSON data...")
        save_json_data(json_file_path, json_data)
        print(f"✓ Successfully normalized {success_count} files and updated JSON.")
    else:
        print("No files were successfully processed.")


def main():
    """Main function to orchestrate the filename normalization process."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Normalize image filenames by removing hash codes',
        epilog='Example: python normalize_filenames.py data.json ./data/imgs'
    )
    parser.add_argument('json_file', help='Path to JSON file containing image references')
    parser.add_argument('data_folder', help='Path to folder containing images')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without modifying files or JSON')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.json_file):
        print(f"Error: JSON file '{args.json_file}' does not exist.")
        sys.exit(1)
    
    if not os.path.exists(args.data_folder):
        print(f"Error: Data folder '{args.data_folder}' does not exist.")
        sys.exit(1)
    
    perform_normalization(args.json_file, args.data_folder, args.dry_run)


if __name__ == "__main__":
    main()