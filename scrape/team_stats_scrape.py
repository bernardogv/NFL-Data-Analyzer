import os
import requests
from bs4 import BeautifulSoup

# Define the base URL for team stats
base_url = "https://www.nfl.com/stats/team-stats/"

# Define the list of stat types and categories for offense, defense, and special-teams
stats_categories = [
    ("offense", ["passing", "rushing", "receiving", "scoring", "downs"]),
    ("defense", ["passing", "rushing", "scoring", "downs", "fumbles", "interceptions"]),
    ("special-teams", ["scoring", "field-goals", "scoring", "kickoffs", "kickoff-returns", "punting", "punt-returns"])
]

# Define the directory structure
base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../team_data/raw_data"))
os.makedirs(base_directory, exist_ok=True)

# Iterate through stat types and categories
for stat_type, categories in stats_categories:
    stats_type_directory = os.path.join(base_directory, stat_type)
    os.makedirs(stats_type_directory, exist_ok=True)

    for category in categories:
        # Construct the URL for the current category and statistics type
        url = f"{base_url}{stat_type}/{category}/2023/reg/all"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table containing the data (you may need to inspect the page source to find the specific table)
            table = soup.find('table', {'class': 'd3-o-table'})

            if table:
                # Save the raw data to a file in the respective folder
                file_path = os.path.join(stats_type_directory, f"{category}.html")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(table))

                print(f"Saved raw data for {stat_type.capitalize()} - Category: {category.capitalize()}")

            else:
                print(f"Table not found on the {stat_type.capitalize()} - {category.capitalize()} page. Skipping.")

        else:
            print(
                f"Failed to retrieve the {stat_type.capitalize()} - {category.capitalize()} webpage. Status code: {response.status_code}")
