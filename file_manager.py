# File Name: file_manager.py
# This file contains all the backend logic for the advanced file manager.

import os
import shutil
import pandas as pd
from pathlib import Path

# =================================================================
# --- Helper and Core Logic Functions ---
# =================================================================

def get_human_readable_size(size_bytes):
    """Converts a file size in bytes to a human-readable format."""
    if size_bytes == 0: return "0 bytes"
    power = 1024
    n = 0
    power_labels = {0: 'bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size_bytes >= power and n < len(power_labels) -1 :
        size_bytes /= power
        n += 1
    return f"{size_bytes:.2f} {power_labels[n]}"

def list_files_as_dataframe(directory):
    """Lists all files and folders in a directory and returns them as a pandas DataFrame."""
    try:
        files = os.listdir(directory)
        data = []
        # Sort folders first, then files, both alphabetically
        for name in sorted(files, key=lambda x: (os.path.isfile(os.path.join(directory, x)), x.lower())):
            path = os.path.join(directory, name)
            if os.path.isdir(path):
                data.append([name, "📁 Folder", "-"])
            else:
                try:
                    size = os.path.getsize(path)
                    size_str = get_human_readable_size(size)
                    data.append([name, "📄 File", size_str])
                except FileNotFoundError:
                    continue # Skip if file was deleted during processing
        
        df = pd.DataFrame(data, columns=["Name", "Type", "Size"])
        return df
    except FileNotFoundError:
        return "Error: The specified directory does not exist."
    except Exception as e:
        return f"An error occurred: {e}"

def rename_item(directory, old_name, new_name):
    """Renames a specified file or folder."""
    old_path = os.path.join(directory, old_name)
    new_path = os.path.join(directory, new_name)
    try:
        if not os.path.exists(old_path):
            return "Error: The file or folder to rename does not exist."
        os.rename(old_path, new_path)
        return "Rename successful."
    except Exception as e:
        return f"Error during rename: {e}"

def delete_item(directory, name):
    """Deletes a specified file or folder."""
    path = os.path.join(directory, name)
    try:
        if os.path.isfile(path):
            os.remove(path)
            return "File deleted successfully."
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return "Directory deleted successfully."
        else:
            return "Error: Item not found."
    except Exception as e:
        return f"Error during deletion: {e}"

def create_directory(directory, folder_name):
    """Creates a new directory in the specified path."""
    path = os.path.join(directory, folder_name)
    try:
        os.makedirs(path, exist_ok=True)
        return f"Directory '{folder_name}' created successfully."
    except Exception as e:
        return f"Error creating directory: {e}"

def get_file_content_for_preview(file_path): # <<< RENAMED THIS FUNCTION
    """Reads and returns the content of a text-based file for previewing."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Cannot read file: {e}"
