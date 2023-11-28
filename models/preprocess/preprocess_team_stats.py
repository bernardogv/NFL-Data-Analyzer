import pandas as pd
import json
import os


def read_and_preprocess_data(category, stat_categories):
    merged_data = pd.DataFrame()
    for stat in stat_categories:
        file_path = f'../../team_data/cleaned_data/{category}/{stat}.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            df = pd.DataFrame(data['team_data'])

            # Perform specific preprocessing steps here
            # ...

            if merged_data.empty:
                merged_data = df
            else:
                # Add suffixes to differentiate columns with the same name
                merged_data = merged_data.merge(df, on='team_name', how='outer', suffixes=('', f'_{stat}'))

    return merged_data

def main():
    stats_categories = [
        ("offense", ["passing", "rushing", "receiving", "scoring", "downs"]),
        ("defense", ["passing", "rushing", "scoring", "downs", "fumbles", "interceptions"]),
        ("special-teams", ["scoring", "field-goals", "kickoffs", "kickoff-returns", "punting", "punt-returns"])
    ]

    for category, stats in stats_categories:
        category_data = read_and_preprocess_data(category, stats)

        # Additional processing if needed
        # ...

        # Save the preprocessed data for each category
        category_data.to_csv(f'../../team_data/preprocessed_data/{category}_preprocessed.csv', index=False)


if __name__ == '__main__':
    main()
