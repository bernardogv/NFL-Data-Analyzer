import pandas as pd

def extract_team_name(value):
    """ Extracts the team name from the given item """
    if isinstance(value, dict):
        return list(value.values())[0].split('\n')[0].strip()
    elif isinstance(value, str):
        return value.split('\n')[0].strip()
    else:
        return None  # or some default value


def clean_data(df, team_name_column):
    """ General cleaning for the defense data """
    # Extracting team name
    df['Team'] = df[team_name_column].apply(lambda x: x.split('\n')[0].strip() if isinstance(x, str) else None)

    # Handling other statistics
    for col in df.columns:
        if col != team_name_column:
            # Assuming other columns contain numeric data directly
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:
            # If it's the team name column, keep only the numeric part
            df[col] = df[col].apply(lambda x: x.split('\n')[-1].strip() if isinstance(x, str) else None)
            df.rename(columns={col: col + '_stat'}, inplace=True)

    return df


def preprocess_defense_data(data_dict):
    """ Preprocesses all defense-related data """
    cleaned_data = {}

    for key, df in data_dict.items():
        team_name_column = df.columns[0]
        cleaned_data[key] = clean_data(df, team_name_column)

    return cleaned_data

def check_data_completeness(preprocessed_data):
    for key, df in preprocessed_data.items():
        print(f"Data for {key}:")
        print("Number of rows (teams):", df.shape[0])
        print("Number of columns (stats):", df.shape[1])
        print("Columns:", df.columns.tolist())
        print()

def check_numeric_conversion(preprocessed_data):
    for key, df in preprocessed_data.items():
        print(f"Numeric Conversion Check for {key}:")
        print(df.describe())  # Summary statistics for numeric columns
        print("NaN values in each column:\n", df.isna().sum())  # NaN counts
        print()

def merge_stats(preprocessed_data):
    merged_df = None
    for key, df in preprocessed_data.items():
        if merged_df is None:
            merged_df = df
        else:
            merged_df = merged_df.merge(df, on='Team', how='outer')
    return merged_df

# Example usage
if __name__ == "__main__":
    raw_data = {
        'downs': pd.DataFrame(pd.read_json('../../team_data/cleaned_data/defense/downs.json')['table_data']),
        'fumbles': pd.DataFrame(pd.read_json('../../team_data/cleaned_data/defense/fumbles.json')['table_data']),
        'interceptions': pd.DataFrame(pd.read_json('../../team_data/cleaned_data/defense/interceptions.json')['table_data']),
        'passing': pd.DataFrame(pd.read_json('../../team_data/cleaned_data/defense/passing.json')['table_data']),
        'rushing': pd.DataFrame(pd.read_json('../../team_data/cleaned_data/defense/rushing.json')['table_data']),
        'scoring': pd.DataFrame(pd.read_json('../../team_data/cleaned_data/defense/scoring.json')['table_data']),
        # ... load other files similarly
    }
    preprocessed_defense = preprocess_defense_data(raw_data)

    # Running checks
    check_data_completeness(preprocessed_defense)
    check_numeric_conversion(preprocessed_defense)

    # Merging stats for overall analysis (if required)
    merged_defense_data = merge_stats(preprocessed_defense)
    print(merged_defense_data.head())
