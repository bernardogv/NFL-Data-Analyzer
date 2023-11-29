import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_nfl_standings(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the standings table - Adjust the selector as needed
    table = soup.find('table', {'class': 'd3-o-table'})

    # Extract the headers
    headers = [header.text.strip() for header in table.find_all('th')]

    # Extract the rows of the table
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        # Split the team name and keep only the last part
        cols[0] = cols[0].split()[-1]
        data.append(cols)

    # Create a DataFrame and return it
    df = pd.DataFrame(data, columns=headers)
    return df

def main():
    url = 'https://www.nfl.com/standings/league/2023/REG'
    standings_df = scrape_nfl_standings(url)

    # Define the path for saving the CSV file
    save_path = '../team_data/raw_data/league_standings'
    os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
    file_name = 'nfl_standings_2023.csv'
    full_path = os.path.join(save_path, file_name)

    # Save the DataFrame to a CSV file
    standings_df.to_csv(full_path, index=False)
    print(f"Standings saved to {full_path}")

if __name__ == "__main__":
    main()
