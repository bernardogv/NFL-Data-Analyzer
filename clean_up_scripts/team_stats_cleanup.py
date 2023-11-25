import os
import json
from bs4 import BeautifulSoup

# Get the current directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Navigate to the 'team_data' directory
team_data_directory = os.path.join(script_directory, "..", "team_data")
os.makedirs(team_data_directory, exist_ok=True)


# Define a function to clean up an HTML file and save as JSON
def clean_and_save_as_json(file_path, cleaned_data_directory):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_data = file.read()

    soup = BeautifulSoup(html_data, 'html.parser')

    # Find the table element in the HTML
    table = soup.find('table')

    if table:
        # Extract table headers as a list
        headers = [header.text.strip() for header in table.find_all('th', scope='col')]

        # Initialize a list to store the table data as dictionaries
        table_data = []

        # Loop through rows to extract and structure the data
        for row in table.find_all('tr'):
            row_data = [cell.text.strip() for cell in row.find_all('td')]
            if row_data:
                # Create a dictionary using headers as keys and row_data as values
                row_dict = {header: value for header, value in zip(headers, row_data)}
                table_data.append(row_dict)

        # Create a dictionary to represent the data
        data_dict = {"table_data": table_data}

        # Determine the JSON file path
        json_filename = os.path.splitext(os.path.basename(file_path))[0] + ".json"
        json_file_path = os.path.join(cleaned_data_directory, json_filename)

        # Convert the data to JSON and save it to a file
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data_dict, json_file, ensure_ascii=False, indent=4)

        print(f"Cleaned data saved as {json_filename}")
    else:
        print("Table not found in the HTML data.")


# Iterate through the categories (defense, offense, special-teams)
categories = ["defense", "offense", "special-teams"]
for category in categories:
    # Define the directory paths for raw and cleaned data
    raw_data_directory = os.path.join(team_data_directory, "raw_data", category)
    cleaned_data_directory = os.path.join(team_data_directory, "cleaned_data", category)
    os.makedirs(cleaned_data_directory, exist_ok=True)

    # Iterate through the raw data directory for the current category
    for root, _, files in os.walk(raw_data_directory):
        for file_name in files:
            if file_name.endswith(".html"):
                file_path = os.path.join(root, file_name)

                # Call the clean_and_save_as_json function to clean up the HTML file and save as JSON
                clean_and_save_as_json(file_path, cleaned_data_directory)

                print(f"Cleaned: {file_path}")

print("Cleaning process completed.")
