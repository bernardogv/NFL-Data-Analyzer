import os
import json
import pandas as pd

def read_json_files(folder_path):
    """Reads all JSON files in a folder and returns a combined DataFrame."""
    data_frames = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                data_frames.append(pd.DataFrame(data))
    return pd.concat(data_frames, ignore_index=True)

def load_all_data(base_path='../team_data/cleaned_data'):
    """Loads data from defense, offense, and special-teams directories."""
    data = {}
    for category in ['defense', 'offense', 'special-teams']:
        folder_path = os.path.join(base_path, category)
        try:
            data[category] = read_json_files(folder_path)
            print(f"Loaded data from {folder_path}")
        except Exception as e:
            print(f"Error loading data from {folder_path}: {e}")
    return data

# Test the function (you can remove this in the final script)
if __name__ == "__main__":
    all_data = load_all_data()
    print(all_data['defense'].head())  # Just as an example to show some data
