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
    table = soup.find('table')

    if table:
        headers = [header.text.strip() for header in table.find_all('th', scope='col')]
        table_data = []

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                row_dict = {}

                # Extract team name from the first cell
                team_name_div = cells[0].find('div', class_='d3-o-club-fullname')
                team_name = team_name_div.text.strip() if team_name_div else ""
                row_dict["team_name"] = team_name

                # Extract statistics from the remaining cells
                for header, cell in zip(headers, cells[1:]):  # Skip the first cell
                    stat = cell.text.strip()
                    row_dict[header] = stat

                table_data.append(row_dict)

        data_dict = {"team_data": table_data}
        json_filename = os.path.splitext(os.path.basename(file_path))[0] + ".json"
        json_file_path = os.path.join(cleaned_data_directory, json_filename)

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
