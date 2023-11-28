import pandas as pd
import json
import os

def clean_and_rename_lng_data(df, category, stat):
    if 'Lng' in df.columns:
        new_column_name = f'{stat}_Lng'
        df[new_column_name] = df['Lng'].str.replace('T', '').astype(float)
        df.drop('Lng', axis=1, inplace=True)
    return df

def calculate_field_goal_percentage(df, field_goal_ranges):
    for range_ in field_goal_ranges:
        col_name = f'{range_} > A-M'

        if col_name in df.columns:
            df[[f'{range_}_Att', f'{range_}_Md']] = df[col_name].str.split('_', expand=True).apply(pd.to_numeric, errors='coerce')
            df[f'{range_}_Pct'] = (df[f'{range_}_Md'] / df[f'{range_}_Att']).fillna(0) * 100
            df.drop(col_name, axis=1, inplace=True)

    return df

def read_and_preprocess_data(category, stat_categories):
    merged_data = pd.DataFrame()
    field_goal_ranges = ['1-19', '20-29', '30-39', '40-49', '50-59', '60+']

    for stat in stat_categories:
        file_path = f'../../team_data/cleaned_data/{category}/{stat}.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            df = pd.DataFrame(data['team_data'])

            # Clean and rename the 'Lng' data
            df = clean_and_rename_lng_data(df, category, stat)

            # Specific preprocessing for field goal stats in special teams
            if category == 'special-teams':
                df = calculate_field_goal_percentage(df, field_goal_ranges)

            if merged_data.empty:
                merged_data = df
            else:
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
        category_data.to_csv(f'../../team_data/preprocessed_data/{category}_preprocessed.csv', index=False)

if __name__ == '__main__':
    main()
